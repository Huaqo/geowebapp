function submitForm() {
    document.getElementById('generate_map').value = "true";
    document.getElementById('filterForm').submit();
}

function submitGroupByForm() {
    document.getElementById('groupByForm').submit();
}

function generateMap() {
    document.getElementById('generate_map').value = "true";
    document.getElementById('filterForm').submit();
}

// Preserve checkbox states on form submission
document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            if (checkbox.checked) {
                checkbox.setAttribute('checked', 'checked');
            } else {
                checkbox.removeAttribute('checked');
            }
        });
    });
    document.getElementById('group_by').addEventListener('change', submitGroupByForm);
});
