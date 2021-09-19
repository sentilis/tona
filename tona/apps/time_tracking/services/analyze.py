import jinja2
import os
from tona.apps.time_tracking.models.time_entry import TimeEntry
from tona.core.model import advance_filters
from datetime import datetime
from tona.utils.dt import convert_datetime, format_duration, format_datetime
from tona.utils.dt import FORMAT_DATE, FORMAT_DATETIME, FORMAT_DATETIME_UTC
from tona.utils.pdf import build_pdf
from tona.utils.csv import build_csv
import tempfile


class Analyze:

    def group_by_any(self, params: dict):
        rows = TimeEntry.select().where(
            TimeEntry.stop != None,
            TimeEntry.res_model == None,
            TimeEntry.res_id == None)
        rows = advance_filters(TimeEntry, rows, params)
        return list(rows)

    def export_csv(self, group_by: str, rows, tz: str):
        lines = []

        duration = 0

        lines.append([group_by.title()])
        lines.append(["Name", "Start", "Stop", "Duration"])
        for row in rows:
            lines.append([
                row.name,
                convert_datetime(format_datetime(row.start, fmt_in=FORMAT_DATETIME_UTC, obj=True), fmt_out=FORMAT_DATETIME, tz_out=tz),
                convert_datetime(format_datetime(row.stop, fmt_in=FORMAT_DATETIME_UTC, obj=True), fmt_out=FORMAT_DATETIME, tz_out=tz),
                format_duration(row.duration),
            ])
            duration += row.duration
        lines.append(["", "", "Total Hours:", format_duration(duration)])
        lines.append([])

        fname = f"Tona Track - {str(group_by).title()} - {datetime.utcnow().timestamp()}.csv"
        content = build_csv(tempfile.gettempdir(), fname, lines)        
        return {
            "path": content, 
            "name": fname
        }


    def export_pdf(self, group_by: str, rows, tz: str):
        path_template = os.path.join(os.path.dirname(__file__), "../templates")
        loader = jinja2.FileSystemLoader(path_template)
        jenv = jinja2.Environment(loader=loader)
        template = jenv.get_or_select_template("analyze_body_pdf.html")
        htmlout = template.render(
            group_by=group_by.title(),
            rows=rows,
            format_duration=format_duration,
            convert_datetime=convert_datetime,
            format_datetime=format_datetime,
            FORMAT_DATETIME=FORMAT_DATETIME,
            FORMAT_DATETIME_UTC=FORMAT_DATETIME_UTC,
            TZ=tz
        )
        
        name = f"Tona Track - {str(group_by).title()} - {datetime.utcnow().timestamp()}.pdf"

        content = build_pdf(tempfile.gettempdir(), name,
                            os.path.join(path_template, "analyze_header_pdf.html"),
                            htmlout,
                            os.path.join(path_template, "analyze_footer_pdf.html"))
        return {
            "path": content, 
            "name": name,
        }
