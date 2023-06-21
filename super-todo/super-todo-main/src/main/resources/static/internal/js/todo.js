
const check_link_availability = () => {
    $.ajax({
        'type': 'POST',
        'contentType': 'application/json',
        'url': '/notes/check-link-availability',
        'data': JSON.stringify({"link": $('#link-input').val()}),
        success: function (response) {
            if (response.success) {
                $('#check-link-message')
                    .empty()
                    .append(
                        `<div class="alert alert-dismissible fade show alert-success" role="alert">
                            <i class="fas fa-flag-checkered"></i>
                            <strong>Success!</strong> Resource link is available now
                            <button type="button" class="btn-close" data-mdb-dismiss="alert" aria-label="Close"></button>
                        </div>`
                    );
            } else {
                $('#check-link-message')
                    .empty()
                    .append(
                        `<div class="alert alert-dismissible fade show alert-danger" role="alert">
                            <i class="fas fa-triangle-exclamation"></i>
                            <strong>Oops!</strong> Resource link is not available now
                            <button type="button" class="btn-close" data-mdb-dismiss="alert" aria-label="Close"></button>
                        </div>`
                    );
            }
        }
    });
}

const toggle_completion_status = (element) => {
    $.ajax({
        'type': 'PATCH',
        'contentType': 'application/json',
        'url': $(element).val(),
        'success': (response) => {
            const titleId = $(element).attr('target-button-heading');
            if(response.isCompleted) {
                $('#' + titleId).addClass('crossed-out');
            } else {
                $('#' + titleId).removeClass('crossed-out');
            }
        }
    });
}

const delete_note_item = (element) => {
    $.ajax({
        'type': 'DELETE',
        'contentType': 'application/json',
        'url': $(element).attr('url'),
        'success': () => {
            $(element).closest("ul").remove();
        }
    });
}


const get_filtering_and_sorting_notes = () => {
    const filter = $('#filter-select').val();
    const sort = $('#sorter-select').val();
    $('#content').load(`/notes?filter=${filter}&sort=${sort} #note-list`);
}
