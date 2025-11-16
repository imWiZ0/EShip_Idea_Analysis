import pdfkit
import json
from datetime import datetime


def convert_to_pdf(data,output_path):
    try:
        output_filename = output_path  
        html_content = generate_html_from_data(data)
        
        try:
            config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
        except:
            config = None
        
        pdfkit.from_string(html_content, output_filename, configuration=config)
        print(f"PDF saved successfully: result.pdf")
        return output_filename
        
    except Exception as e:
        print(f"Error converting to PDF: {e}")
        return None



def generate_html_from_data(data):
    
    html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="utf-8">
        <title>تقرير تحليل الفكرة</title>
        <style>
            body {
                font-family: 'Arial Unicode MS', sans-serif;
                direction: rtl;
                margin: 40px;
                background: white;
                color: #333;
                font-size: 22px;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
                border-bottom: 3px solid #7b2ff7;
                padding-bottom: 20px;
            }
            .header h1 {
                color: #7b2ff7;
                font-size: 36px;
                margin: 0;
            }
            .section {
                margin: 30px 0;
                page-break-inside: avoid;
            }
            .section-title {
                background: linear-gradient(135deg, #7b2ff7, #2bc0ff);
                color: white;
                padding: 18px;
                border-radius: 5px;
                font-size: 26px;
                font-weight: bold;
                margin-bottom: 15px;
            }
            .content {
                background: #f5f5f5;
                padding: 20px;
                border-radius: 5px;
                line-height: 2.0;
                font-size: 22px;
            }
            .stat-row {
                display: flex;
                justify-content: space-around;
                margin: 15px 0;
            }
            .stat {
                text-align: center;
                flex: 1;
                padding: 14px;
                background: white;
                border-radius: 5px;
                margin: 0 5px;
            }
            .stat-value {
                font-size: 38px;
                font-weight: bold;
                color: #7b2ff7;
            }
            .stat-label {
                font-size: 22px;
                color: #666;
                margin-top: 5px;
                font-weight: bold;
            }
            ul, ol {
                padding-right: 20px;
                font-size: 22px;
            }
            li {
                margin: 12px 0;
                font-size: 22px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>تقرير تحليل الفكرة</h1>
            <p>إعداد: نظام تحليل الأفكار الريادية</p>
            <p>من قبل: فهد السيف</p>
        </div>
    """
    
    if 'idea_analysis' in data or 'idea analysis' in data:
        idea = data.get('idea_analysis', data.get('idea analysis', {}))
        html += f"""
        <div class="section">
            <div class="section-title">تحليل الفكرة</div>
            <div class="content">
                <p><strong>العنوان:</strong> {idea.get('title', 'N/A')}</p>
                <p><strong>الوصف:</strong> {idea.get('description', 'N/A')}</p>
                <p><strong>الصناعة:</strong> {idea.get('industry', 'N/A')}</p>
                <p><strong>التخصص:</strong> {idea.get('niche', 'N/A')}</p>
                <p><strong>التعليق:</strong> {idea.get('comment', 'N/A')}</p>
            </div>
        </div>
        """
    
    if 'market_analysis' in data:
        market = data['market_analysis']
        html += f"""
        <div class="section">
            <div class="section-title">تحليل السوق</div>
            <div class="content">
                    <div class='stat-row' style='display: flex; flex-direction: row; justify-content: space-between; gap: 24px; margin-bottom: 18px;'>
                        <div class='stat' style='flex:1; text-align:center;'>
                            <div class='stat-value' style='font-size:32px; font-weight:900; color:#2b2ff7; margin-bottom:8px;'>{market.get('size', 'N/A')}</div>
                            <div class='stat-label' style='font-size:18px; font-weight:bold;'>حجم السوق</div>
                        </div>
                        <div class='stat' style='flex:1; text-align:center;'>
                            <div class='stat-value' style='font-size:32px; font-weight:900; color:#2b2ff7; margin-bottom:8px;'>{market.get('demand', 'N/A')}</div>
                            <div class='stat-label' style='font-size:18px; font-weight:bold;'>الطلب</div>
                        </div>
                        <div class='stat' style='flex:1; text-align:center;'>
                            <div class='stat-value' style='font-size:32px; font-weight:900; color:#2b2ff7; margin-bottom:8px;'>{market.get('growth', 'N/A')}</div>
                            <div class='stat-label' style='font-size:18px; font-weight:bold;'>النمو</div>
                        </div>
                    </div>
                <p><strong>التعليق:</strong> {market.get('comment', 'N/A')}</p>
            </div>
        </div>
        """
    
    if 'competitors' in data:
        comp = data['competitors']
        competitors_list = ""
        if isinstance(comp.get('name'), list):
            competitors_list = "".join([f"<li>{c}</li>" for c in comp.get('name', [])])
        
        features_list = ""
        if isinstance(comp.get('features'), list):
            features_list = "".join([f"<li>{f}</li>" for f in comp.get('features', [])])
        
        html += f"""
        <div class="section">
            <div class="section-title">المنافسون</div>
            <div class="content">
                <p><strong>التعليق:</strong> {comp.get('comment', 'N/A')}</p>
                <p><strong>القوة:</strong> {comp.get('strength', 'N/A')} | <strong>العدد:</strong> {comp.get('count', 'N/A')}</p>
                <p><strong>المنافسون الرئيسيون:</strong></p>
                <ul>{competitors_list if competitors_list else "<li>لا توجد بيانات</li>"}</ul>
                <p><strong>الميزات الرئيسية:</strong></p>
                <ul>{features_list if features_list else "<li>لا توجد بيانات</li>"}</ul>
            </div>
        </div>
        """
    
    if 'audience' in data:
        audience = data['audience']
        html += f"""
        <div class="section">
            <div class="section-title">الجمهور المستهدف</div>
            <div class="content">
                <p><strong>الفئة العمرية:</strong> {audience.get('age_range', 'N/A')}</p>
                <p><strong>الدولة:</strong> {audience.get('country', 'N/A')}</p>
                <p><strong>القوة الشرائية:</strong> {audience.get('buying_power', 'N/A')}</p>
                <p><strong>نسبة القبول:</strong> {audience.get('acceptance_probability', 'N/A')}%</p>
                <p><strong>التعليق:</strong> {audience.get('comment', 'N/A')}</p>
            </div>
        </div>
        """
    
    if 'costs' in data:
        costs = data['costs']
        html += f"""
        <div class="section">
            <div class="section-title">التكاليف</div>
            <div class="content">
                <p><strong>تكلفة البدء:</strong> {costs.get('startup', 'N/A')}</p>
                <p><strong>التكاليف الشهرية:</strong> {costs.get('running', 'N/A')}</p>
                <p><strong>التعليق:</strong> {costs.get('comment', 'N/A')}</p>
            </div>
        </div>
        """
    
    if 'risks' in data:
        risks = data['risks']
        html += f"""
        <div class="section">
            <div class="section-title">المخاطر</div>
            <div class="content">
                <p><strong>التعليق:</strong> {risks.get('comment', 'N/A')}</p>
            </div>
        </div>
        """
    
    if 'final' in data:
        final = data['final']
        feasible = "نعم" if final.get('feasible') else "لا"
        html += f"""
        <div class="section">
            <div class="section-title">التقييم النهائي</div>
            <div class="content">
                <p><strong>قابلة للتنفيذ:</strong> {feasible}</p>
                <p><strong>درجة الثقة:</strong> {final.get('confidence', 'N/A')}</p>
                <p><strong>الخلاصة:</strong> {final.get('summary', 'N/A')}</p>
            </div>
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    
    return html



