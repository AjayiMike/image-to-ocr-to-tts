

function getTaskId() {
    return localStorage.getItem('task_id');
}
function setTaskId(_task_id) {
    return localStorage.getItem(_task_id);
}
// setTaskId();

// [io] should already be included on page load (included in index.html).
const socket = io();

socket.on("connect", (msg) => {
    console.log("connected to websocket server with id:", socket.id, msg);
});


// "IMAGE_TASK_ID" would be declared in index.html jinja template
if (IMAGE_TASK_ID) {
    console.log("[GOT IMAGE_TASK_ID]: ", IMAGE_TASK_ID);
    socket.emit("status", { _client_id: window.USER_ID, _task_id: WEBSOCKET_TASK_ID });
}

socket.on("status", { _client_id: window.USER_ID, _task_id: WEBSOCKET_TASK_ID }, (_task) => {
    console.log(_task);
    const task = JSON.parse(_task) | null;

    // emit('status', {'_task_id': task_id, 'error': 'true', 'message':'invalid task id'});
    if (task === null || task.error) {
        alert("Unknown Task ID!!");
        return;
    }

    // emit('status', {'_task_id': task_id, 'done': 'false', 'message':text_result, 'progress': 65});
    else if (task.done == 'false') {
        console.log("[%]: ", task.progress);
        progressUpdate(task.progress);
    }

    // emit('status', {'_task_id': task_id, 'error': 'false', 'message':audio_file_url , 'done': 'true'});
    else if (task.done === 'true') {
        taskCompleted(task.message)
    }

})

function progressUpdate(_percent_done) {

}


function taskCompleted(audio_file_url) {
    const els = document.getElementsByClassName('audio-section');
    // Make the audio player visible.
    for (let index = 0; index < els.length; index++) {
        const element = els[index];
        element.classList.remove('hidden');
    }
    initializeAudioPlayer(audio_file_url);
}