let CURRENT_TASK_ID = 0;

function getTaskId() {
    return localStorage.getItem("task_id");
}
function setTaskId(_task_id) {
    return localStorage.getItem(_task_id);
}
// setTaskId();

// [io] should already be included on page load (included in index.html).
const socket = io();

socket.on("connect", () => {
    console.log("connected to websocket server with id:", socket.id);
});

// "IMAGE_TASK_ID" would be declared in index.html jinja template
if (IMAGE_TASK_ID) {
    console.log("[GOT IMAGE_TASK_ID]: ", IMAGE_TASK_ID);

    // We signify server to start task processing, passing along the task id.
    socket.emit("status", { _task_id: IMAGE_TASK_ID });
    CURRENT_TASK_ID = IMAGE_TASK_ID;
}

socket.on("status", (_task) => {
    console.log(_task);
    const task = _task;

    // emit('status', {'_task_id': task_id, 'error': 'true', 'message':'invalid task id'});
    if (task === null || task.error === "true") {
        errorUpdate(task.message);
        return;
    }

    // emit('status', {'_task_id': task_id, 'done': 'false', 'message':text_result, 'progress': 65});
    else if (task.done == "false") {
        console.log("[%]: ", task.progress);
        progressUpdate(Number.parseInt(task.progress));
    }

    // emit('status', {'_task_id': task_id, 'error': 'false', 'message':audio_file_url , 'done': 'true'});
    else if (task.done === "true") {
        progressUpdate(100);
        taskCompleted(task.message);
    }

    // "payload" is only provided when server returns pdf and text content.
    // if (task.payload && _task_id === CURRENT_TASK_ID) {
    if (task.payload) {
        // Populate 'textarea' display
        const text_content_wrapper = document.querySelector(
            "#text-content-wrapper"
        );
        text_content_wrapper.classList.replace("hidden", "block");
        const display_area = document.getElementById("text-content");
        display_area.textContent = task.payload.message;

        // Setup and show PDF download link
        const pdf_download_url = document.getElementById("pdf_download_url");
        pdf_download_url.classList.remove("hidden");

        // Update the link.
        pdf_download_url.setAttribute("href", task.payload.pdf_url);
    }
});

function progressUpdate(_percent_done) {
    const progress_indicator = document.getElementById("progress-indicator");
    const submit_button = document.getElementById("submit-btn");
    const percent_done = _percent_done >= 100 ? 100 : _percent_done;

    progress_indicator.style.width = percent_done + "%";
    submit_button.setAttribute("value", "Processing ... " + percent_done + "%");

    if (_percent_done === 100)
        setTimeout(() => submit_button.setAttribute("value", "Upload"), 2500);
}

function taskCompleted(audio_file_url) {
    const audio_section = document.getElementById("audio-section");
    const audio_player_el = document.getElementById("audio_player");
    const file_url_el = document.getElementById("file_url");

    // Make the audio player section visible.
    audio_section.classList.remove("hidden");

    // Set audio file download link.
    file_url_el.setAttribute("href", audio_file_url);

    // Set audio player source file.
    audio_player_el.setAttribute("src", audio_file_url);
    audio_player_el.parentElement.load();
}

function errorUpdate(_error_msg) {
    const progress_indicator = document.getElementById("progress-indicator");
    const submit_button = document.getElementById("submit-btn");

    progress_indicator.style.width = "0%";
    progress_indicator.parentElement.style.backgroundColor = "crimson";
    submit_button.setAttribute("value", _error_msg);

    // Change text to "UPLOAD" after 2 seconds.
    setTimeout(() => {
        progress_indicator.parentElement.style.backgroundColor = "#60a5fa";
        submit_button.setAttribute("value", "UPLOAD");
    }, 2500);
}

/*
Handles a click on the song played progress bar.
*/
