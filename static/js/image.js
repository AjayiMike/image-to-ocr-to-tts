let image_preview_wrapper,
    image_preview,
    image_input,
    cancel_icon_wrapper,
    cancel_icon;
const placeholder_image =
    "https://placehold.co/600x400?text=Select+an+Image+With+Text";

const init = () => {
    image_input = document.querySelector("#image_input");
    image_preview = document.querySelector("#image_preview");
    image_preview_wrapper = document.querySelector("#image_preview_wrapper");
    cancel_icon = document.querySelector("#cancel_icon");
    cancel_icon_wrapper = document.querySelector("#cancel_icon_wrapper");
    image_preview.setAttribute("src", placeholder_image);
    console.log("Ready!");
};

window.onload = init();

const handle_image_preview_wrapper_click = () => {
    image_input.click();
};

const readURL = (e) => {
    const { target } = e;
    if (target.files && target.files[0]) {
        const reader = new FileReader();

        reader.onload = (e) => {
            image_preview.setAttribute("src", e.target.result);
            cancel_icon_wrapper.classList.replace("hidden", "block");
        };

        reader.readAsDataURL(target.files[0]);
    } else {
        image_preview.setAttribute("src", e.target.result);
        cancel_icon_wrapper.classList.replace("block", "hidden");
    }
};
image_preview_wrapper.addEventListener(
    "click",
    handle_image_preview_wrapper_click
);
image_input.addEventListener("change", readURL);
