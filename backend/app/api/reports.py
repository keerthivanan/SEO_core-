from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import Response
from app.services.pdf_generator import PDFGenerator
from app.services.database import db

router = APIRouter()
pdf_generator = PDFGenerator()

@router.get("/reports/{analysis_id}/download")
async def download_report(analysis_id: str):
    """
    Generates and downloads a PDF report for a specific analysis using LIVE data.
    """
    try:
        # Fetch from DB:
        record = await db.get_analysis(analysis_id)
        
        if not record:
            raise HTTPException(status_code=404, detail="Analysis report not found.")

        # Reconstruct analysis data from DB record
        # Note: report_data contains the full dict with all sub-analysis (AEO, GEO, Semantic)
        analysis_data = record.get('report_data', record)
        
        # Generate PDF
        pdf_bytes = await pdf_generator.generate_report(analysis_data)
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=report-{analysis_id}.pdf"}
        )
        
    except Exception as e:
        print(f"PDF Generation Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
