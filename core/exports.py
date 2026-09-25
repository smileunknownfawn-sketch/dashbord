from __future__ import annotations

from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Iterable


def csv_bytes(rows: Iterable[dict], columns: list[tuple[str, str]]) -> bytes:
    import csv
    import io
    stream = io.StringIO()
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow([title for title, _ in columns])
    for row in rows:
        writer.writerow([row.get(key, "") for _, key in columns])
    return stream.getvalue().encode("utf-8-sig")


def xlsx_bytes(rows: Iterable[dict], columns: list[tuple[str, str]]) -> bytes:
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Розпорядження"
    ws.append([title for title, _ in columns])
    for row in rows:
        ws.append([row.get(key, "") for _, key in columns])
    for cell in ws[1]:
        cell.font = cell.font.copy(bold=True)
    for col in ws.columns:
        letter = col[0].column_letter
        ws.column_dimensions[letter].width = min(max(max(len(str(c.value or "")) for c in col) + 2, 12), 42)
    output = BytesIO()
    wb.save(output)
    return output.getvalue()


def pdf_bytes(rows: Iterable[dict], columns: list[tuple[str, str]], title: str = "Звіт") -> bytes:
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=landscape(A4), leftMargin=24, rightMargin=24, topMargin=24, bottomMargin=24)
    styles = getSampleStyleSheet()
    data = [[title] + [""] * (len(columns) - 1), [x[0] for x in columns]]
    for row in rows:
        data.append([str(row.get(key, "")) for _, key in columns])
    table = Table(data, repeatRows=2)
    table.setStyle(TableStyle([
        ("SPAN", (0, 0), (-1, 0)), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#18251d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#d7bd70")),
        ("GRID", (0, 1), (-1, -1), .35, colors.HexColor("#888888")), ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BOTTOMPADDING", (0, 0), (-1, 0), 9),
    ]))
    doc.build([Paragraph(title, styles["Title"]), Spacer(1, 8), table])
    return output.getvalue()


def filename(prefix: str, extension: str) -> str:
    return f"{prefix}_{datetime.now():%Y%m%d_%H%M%S}.{extension}"
