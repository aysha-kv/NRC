import frappe


@frappe.whitelist()
def get_user_projects():
    user = frappe.session.user

    project_links = frappe.get_all(
        "Project User",
        filters={"user": user},
        fields=["parent"]
    )

    project_names = [p.parent for p in project_links]

    if not project_names:
        return []

    return frappe.get_all(
        "Project",
        filters={"name": ["in", project_names]},
        fields=["name", "project_name", "status", "percent_complete"]
    )


@frappe.whitelist()
def get_project_details(project):
    user = frappe.session.user

    if not frappe.db.exists("Project User", {"parent": project, "user": user}):
        frappe.throw("Not permitted")

    proj = frappe.get_doc("Project", project)

    tasks = frappe.get_all(
        "Task",
        filters={"project": project},
        fields=["name", "subject", "status"]
    )

    ts_details = frappe.get_all(
        "Timesheet Detail",
        filters={"project": project},
        fields=["parent"]
    )

    ts_names = list(set([t.parent for t in ts_details]))

    timesheets = []
    if ts_names:
        timesheets = frappe.get_all(
            "Timesheet",
            filters={"name": ["in", ts_names]},
            fields=["name", "employee", "total_hours"]
        )

    attachments = frappe.get_all(
        "File",
        filters={
            "attached_to_doctype": "Project",
            "attached_to_name": project
        },
        fields=["file_name", "file_url"]
    )

    return {
        "project_name": proj.project_name,
        "status": proj.status,
        "percent_complete": proj.percent_complete,
        "tasks": tasks,
        "timesheets": timesheets,
        "attachments": attachments
    }