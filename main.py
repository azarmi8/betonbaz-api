"""
🏗️ SSG-Nexus Backend (FastAPI)
سیستم کنترل کیفیت بتن مدرن برای صنعت ساخت‌وساز
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Optional, List
from datetime import datetime
import numpy as np
import pandas as pd

# ── کتابخانه‌های خارجی ──
from supabase import create_client, Client
from groq import Groq

# ════════════════════════════════════════════
# تنظیمات FastAPI
# ════════════════════════════════════════════
app = FastAPI(
    title="SSG-Nexus Concrete QC API",
    description="سیستم کنترل کیفیت بتن برای صنعت ساخت‌وساز",
    version="1.0.0"
)

# ── CORS برای فرانت‌اند ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ════════════════════════════════════════════
# متغیرهای محیطی (الزامی)
# ════════════════════════════════════════════
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ خطای حیاتی: متغیرهای SUPABASE_URL یا SUPABASE_KEY یافت نشدند!")
    print("✅ اطمینان دهید که در Render Environment Variables این‌ها را تعریف کرده‌اید.")
    exit(1)

# ── کلاینت‌ها ──
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase متصل شد")
except Exception as e:
    print(f"❌ خطا در اتصال Supabase: {e}")
    exit(1)

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if groq_client:
    print("✅ Groq AI متصل شد")
else:
    print("⚠️ Groq API Key یافت نشد - سرویس AI غیرفعال")

# ════════════════════════════════════════════
# مدل‌های داده (Pydantic)
# ════════════════════════════════════════════
class Project(BaseModel):
    client_name: str
    address: str
    location: Optional[str] = None
    link: Optional[str] = None

class ConcreteResult(BaseModel):
    project_name: str
    client_name: str
    project_address: str
    mix_code: str
    strength_grade: int
    pour_date: str
    cube_7_1: Optional[float] = None
    cube_7_2: Optional[float] = None
    cube_28_1: Optional[float] = None
    cube_28_2: Optional[float] = None
    cube_28_3: Optional[float] = None

class FieldReport(BaseModel):
    project_name: str
    client_name: str
    slump: float
    temperature: float
    mix_code: str
    image_urls: List[str]
    notes: Optional[str] = None
    timestamp: Optional[str] = None

class AIQuestion(BaseModel):
    question: str

# ════════════════════════════════════════════
# توابع کمکی
# ════════════════════════════════════════════
def _fmt(val):
    return f"{val:.2f}" if val is not None else "—"

def _avg(vals: list):
    valid = [v for v in vals if v is not None]
    return sum(valid) / len(valid) if valid else None

def _std(vals: list):
    valid = [v for v in vals if v is not None]
    if len(valid) < 2:
        return None
    return float(np.std(valid))

def _validate_images(image_urls: List[str]) -> bool:
    if not image_urls:
        return False
    return all(isinstance(url, str) and len(url) > 0 for url in image_urls)

# ════════════════════════════════════════════
# Health Check & Root
# ════════════════════════════════════════════
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "supabase": "connected",
        "groq": "available" if groq_client else "unavailable"
    }

@app.get("/")
def root():
    return {
        "name": "SSG-Nexus Concrete QC API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

# ════════════════════════════════════════════
# پروژه‌ها (Projects)
# ════════════════════════════════════════════
@app.post("/api/projects", tags=["Projects"])
def create_project(project: Project):
    try:
        data = project.dict()
        data["created_at"] = datetime.now().isoformat()
        response = supabase.table("projects").insert(data).execute()
        return {"status": "success", "project": response.data[0] if response.data else None}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/projects", tags=["Projects"])
def get_projects():
    try:
        response = supabase.table("projects").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/projects/{project_id}", tags=["Projects"])
def get_project(project_id: int):
    try:
        response = supabase.table("projects").select("*").eq("id", project_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="پروژه یافت نشد")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ════════════════════════════════════════════
# نتایج آزمایشگاه (Concrete Results)
# ════════════════════════════════════════════
@app.post("/api/results", tags=["Lab Results"])
def add_concrete_result(result: ConcreteResult):
    try:
        data = result.dict()
        data["created_at"] = datetime.now().isoformat()
        response = supabase.table("concrete_results").insert(data).execute()
        return {"status": "success", "result": response.data[0] if response.data else None}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/results", tags=["Lab Results"])
def get_concrete_results(
    mix_code: Optional[str] = None,
    strength_grade: Optional[int] = None,
    project_name: Optional[str] = None,
    limit: int = 100
):
    try:
        query = supabase.table("concrete_results").select("*")
        if mix_code: query = query.eq("mix_code", mix_code)
        if strength_grade: query = query.eq("strength_grade", strength_grade)
        if project_name: query = query.ilike("project_name", f"%{project_name}%")
        response = query.order("created_at", desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/results/{result_id}", tags=["Lab Results"])
def get_result(result_id: int):
    try:
        response = supabase.table("concrete_results").select("*").eq("id", result_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="نتیجه یافت نشد")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ════════════════════════════════════════════
# گزارش‌های تصویری (Field Reports)
# ════════════════════════════════════════════
@app.post("/api/field-reports", tags=["Field Reports"])
def add_field_report(report: FieldReport):
    if not _validate_images(report.image_urls):
        raise HTTPException(status_code=400, detail="حداقل یک لینک عکس معتبر الزامی است")
    try:
        data = report.dict()
        data["created_at"] = datetime.now().isoformat()
        response = supabase.table("field_reports").insert(data).execute()
        return {"status": "success", "report": response.data[0] if response.data else None}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/field-reports", tags=["Field Reports"])
def get_field_reports(project_name: Optional[str] = None, limit: int = 50):
    try:
        query = supabase.table("field_reports").select("*")
        if project_name: query = query.ilike("project_name", f"%{project_name}%")
        response = query.order("created_at", desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/field-reports/{report_id}", tags=["Field Reports"])
def get_field_report(report_id: int):
    try:
        response = supabase.table("field_reports").select("*").eq("id", report_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="گزارش یافت نشد")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ════════════════════════════════════════════
# آنالیتیکس و داشبورد
# ════════════════════════════════════════════
@app.get("/api/dashboard", tags=["Analytics"])
def get_dashboard_data():
    try:
        results = supabase.table("concrete_results").select("*").execute()
        data = results.data
        if not data:
            return {"total_tests": 0, "total_projects": 0, "average_28_day": None, "mix_codes": [], "strength_distribution": {}, "recent_results": []}
        
        df = pd.DataFrame(data)
        avg_28_day_values = []
        for _, row in df.iterrows():
            cubes = [row.get('cube_28_1'), row.get('cube_28_2'), row.get('cube_28_3')]
            avg = _avg(cubes)
            if avg: avg_28_day_values.append(avg)
        
        return {
            "total_tests": len(data),
            "total_projects": int(df['project_name'].nunique()) if len(df) > 0 else 0,
            "average_28_day": _fmt(_avg(avg_28_day_values)) if avg_28_day_values else None,
            "mix_codes": df['mix_code'].unique().tolist() if len(df) > 0 else [],
            "strength_distribution": df['strength_grade'].value_counts().to_dict() if len(df) > 0 else {},
            "recent_results": data[-10:]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/analytics/mix-code/{mix_code}", tags=["Analytics"])
def get_mix_code_analytics(mix_code: str):
    try:
        response = supabase.table("concrete_results").select("*").eq("mix_code", mix_code).execute()
        data = response.data
        if not data:
            raise HTTPException(status_code=404, detail="داده‌ای یافت نشد")
        
        df = pd.DataFrame(data)
        cube_7_1_values = [v for v in df['cube_7_1'].tolist() if v is not None]
        cube_7_2_values = [v for v in df['cube_7_2'].tolist() if v is not None]
        cube_28_1_values = [v for v in df['cube_28_1'].tolist() if v is not None]
        cube_28_2_values = [v for v in df['cube_28_2'].tolist() if v is not None]
        cube_28_3_values = [v for v in df['cube_28_3'].tolist() if v is not None]
        
        all_7_day = cube_7_1_values + cube_7_2_values
        all_28_day = cube_28_1_values + cube_28_2_values + cube_28_3_values
        
        return {
            "mix_code": mix_code,
            "total_batches": len(data),
            "strength_7_day": {
                "average": _fmt(_avg(all_7_day)) if all_7_day else None,
                "std": _fmt(_std(all_7_day)) if all_7_day else None,
                "min": _fmt(min(all_7_day)) if all_7_day else None,
                "max": _fmt(max(all_7_day)) if all_7_day else None,
            },
            "strength_28_day": {
                "average": _fmt(_avg(all_28_day)) if all_28_day else None,
                "std": _fmt(_std(all_28_day)) if all_28_day else None,
                "min": _fmt(min(all_28_day)) if all_28_day else None,
                "max": _fmt(max(all_28_day)) if all_28_day else None,
            },
            "all_results": data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ════════════════════════════════════════════
# مشاور هوشمند (Groq AI)
# ════════════════════════════════════════════
SYSTEM_PROMPT = """تو یک مشاور فنی متخصص در حوزه بتن و مهندسی عمران هستی. نام تو «دستیار فنی بتن‌باز» است.
به سوالات مهندسان کارگاهی درباره موضوعات زیر پاسخ می‌دهی:
- طرح اختلاط بتن (Mix Design) و رئولوژی
- استانداردهای ACI، ASTM، EN و ایران
- اسلامپ، مقاومت فشاری، نسبت آب به سیمان
- بتن‌ریزی در شرایط گرم و سرد
- کنترل کیفیت (QC) در کارگاه
پاسخ‌ها باید به فارسی، کوتاه و عملی باشند. اگر سوال غیر مرتبط بود، مودبانه توضیح بده."""

@app.post("/api/ask", tags=["AI"])
def ask_ai(item: AIQuestion):
    if not groq_client:
        raise HTTPException(status_code=503, detail="سرویس Groq در دسترس نیست")
    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": item.question}
            ],
            max_tokens=512,
            temperature=0.7
        )
        return {
            "question": item.question,
            "answer": response.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
