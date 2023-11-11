async function uploadImage() {
    let formData = new FormData(document.getElementById("image"));

    // You can add additional form data if needed
    // formData.append('key', 'value');

    const res = fetch("/");

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload", true);
}
