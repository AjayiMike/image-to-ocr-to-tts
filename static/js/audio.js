// if (audio_file_url) {

//     console.log("[INITIALIZING PLAYER]: ", audio_file_url);

//     Amplitude.init({
//         bindings: {
//             37: "prev",
//             39: "next",
//             32: "play_pause",
//         },
//         songs: [
//             {
//                 name: "Risin' High (feat Raashan Ahmad)",
//                 artist: "Ancient Astronauts",
//                 album: "We Are to Answer",
//                 url: audio_file_url,
//                 cover_art_url:
//                     "https://521dimensions.com/img/open-source/amplitudejs/album-art/we-are-to-answer.jpg",
//             },
//         ],
//     });
// }

function initializeAudioPlayer(audio_file_url) {
    /*
        Handles a click on the song played progress bar.
    */
    const player = document.getElementById("song-played-progress");
    console.log(player);
    player.addEventListener("click", function (e) {

        console.log("[INITIALIZE LISTENER]: ", "song-played-progress");

        var offset = this.getBoundingClientRect();
        var x = e.pageX - offset.left;

        Amplitude.setSongPlayedPercentage(
            (parseFloat(x) / parseFloat(this.offsetWidth)) * 100
        );
    });


    if (audio_file_url) {

        console.log("[INITIALIZING PLAYER]: ", audio_file_url);

        Amplitude.init({
            bindings: {
                37: "prev",
                39: "next",
                32: "play_pause",
            },
            songs: [
                {
                    name: "Risin' High (feat Raashan Ahmad)",
                    artist: "Ancient Astronauts",
                    album: "We Are to Answer",
                    url: audio_file_url,
                    cover_art_url:
                        "https://521dimensions.com/img/open-source/amplitudejs/album-art/we-are-to-answer.jpg",
                },
            ],
        });
    }
}

window.onkeydown = function (e) {
    return !(e.keyCode == 32);
};

/*
Handles a click on the song played progress bar.
*/
document
    .getElementById("song-played-progress")
    .addEventListener("click", function (e) {

        console.log("[INITIALIZE LISTENER]: ", "song-played-progress");

        var offset = this.getBoundingClientRect();
        var x = e.pageX - offset.left;

        Amplitude.setSongPlayedPercentage(
            (parseFloat(x) / parseFloat(this.offsetWidth)) * 100
        );
    });
