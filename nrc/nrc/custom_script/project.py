

def calculate_project_progress(doc, method=None):

    tables = [
        "custom_raw_material_quality_inspection",
        "custom_engineering_verification",
        "custom_subcontracting_operations_management",
        "custom_production_machine_management",
        "custom_final_quality_inspection",
    ]

    item_progress_map = {}

    for table in tables:
        for row in doc.get(table) or []:

            item = row.item
            progress = row.progress or 0  

            if not item:
                continue

            if item not in item_progress_map:
                item_progress_map[item] = []

            item_progress_map[item].append(progress)

    total_progress = 0
    item_count = 0

    for row in doc.get("custom_project_progress_summary") or []:

        item = row.item
        progress_list = item_progress_map.get(item, [])

        if progress_list:
            row.inidvidual_progress = sum(progress_list) / len(progress_list)
        else:
            row.inidvidual_progress = 0

        total_progress += row.inidvidual_progress
        item_count += 1

    if item_count:
        doc.percent_complete = total_progress / item_count
    else:
        doc.percent_complete = 0




def sync_project_tables(doc, method):

    target_tables = [
        "custom_raw_material_quality_inspection",
        "custom_engineering_verification",
        "custom_subcontracting_operations_management",
        "custom_production_machine_management",
        "custom_final_quality_inspection",
        "custom_customer_satisfaction_report"
    ]

    source_rows = doc.get("custom_project_progress_summary") or []

    for table in target_tables:
        target_rows = doc.get(table) or []

        while len(target_rows) > len(source_rows):
            target_rows.pop()

        for i, src in enumerate(source_rows):

            if i < len(target_rows):
                target_rows[i].assembly = src.assembly
                target_rows[i].sub_assembly = src.sub_assembly
                target_rows[i].item = src.item
                target_rows[i].drawing_no = src.drawing_no
                target_rows[i].raw_material_grade = src.raw_material_grade

            else:
                doc.append(table, {
                    "assembly": src.assembly,
                    "sub_assembly": src.sub_assembly,
                    "item": src.item,
                    "drawing_no": src.drawing_no,
                    "raw_material_grade": src.raw_material_grade
                })


def calculate_overall_progress(doc, method):
    total_progress = 0
    count = 0

    for row in doc.get("custom_project_progress_summary") or []:
        if row.inidvidual_progress is not None:
            total_progress += row.inidvidual_progress
            count += 1

    doc.custom_overall_progress = (total_progress / count) if count else 0