frappe.ui.form.on('Customer Satisfaction Report', {
    hospitality: calculate,
    communication: calculate,
    quality: calculate,
    management: calculate
});

function calculate(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    let values = [
        row.hospitality,
        row.communication,
        row.quality,
        row.management
    ].filter(v => v != null);

    if (values.length > 0) {
        let total = values.reduce((a, b) => flt(a) + flt(b), 0);
        let avg = total / values.length;

        frappe.model.set_value(cdt, cdn, 'total_score', total);
        frappe.model.set_value(cdt, cdn, 'average_score', avg);
    } else {
        frappe.model.set_value(cdt, cdn, 'total_score', 0);
        frappe.model.set_value(cdt, cdn, 'average_score', 0);
    }
}
