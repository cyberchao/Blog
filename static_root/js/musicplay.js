



/**
 * Based on the class list for a given element toggle the class(es) received.
 * Can accept both string with classes separated by spaces and an array of classes.
 *
 * @param {} element The dom element for which to toggle classes.
 * @param {string|string[]} classes The classes to be toggled on or off.
 */
function toggleClasses(element, classes) {
    const currentClasses = new Set(element.classList);
    // Separate string formatted classes into an array or accept array param
    const newClasses = _.isString(classes) ? classes.split(' ') : classes;

    for (const className of newClasses) {
        if (currentClasses.has(className)) {
            element.classList.remove(className);
        } else {
            element.classList.add(className);
        }
    }
}

/**
 * Toggle a boolean value.
 *
 * @param {boolean} boolean The boolean value to be toggled true or false.
 * @return {boolean} Returns the opposite boolean value to the received.
 */
function toggleBoolean(boolean) {
    return !boolean;
}

/**
 * Convert seconds into a usable format for time.
 *
 * @param {number|string} seconds The amount of seconds to convert.
 * @return {string} Returns a time formatted string (--:--:--).
 */
function secondsToHms(seconds) {
    const time = {
        hours: String(Math.floor(Number(seconds) / 3600)),
        minutes: String(Math.floor(Number(seconds) % 3600 / 60)),
        seconds: String(Math.floor(Number(seconds) % 3600 % 60))
    };


    if (time.hours && time.hours < 10) {
        time.hours = `0${time.hours}`;
    }
    if (time.minutes && time.minutes < 10) {
        time.minutes = `0${time.minutes}`;
    }
    if (time.seconds && time.seconds < 10) {
        time.seconds = `0${time.seconds}`;
    }

    if (time.hours !== '00') {
        return `${time.hours}:${time.minutes}:${time.seconds}`;
    } else {
        return `${time.minutes}:${time.seconds}`;
    }
}

/**
 * The base setup for any given audio player.
 */
class Player {
    constructor() {
        this.playing = new Set(buttons.playPause.classList).has('on');
        this.shuffle = new Set(buttons.shuffle.classList).has('on');
        this.repeat = new Set(buttons.repeat.classList).has('on');

        this.songIndex = 0;
        this.previousSong = songList.length - 1;

        this.song = songList[this.songIndex];

        this.randomOrder = new Set();
        this.randomIndex = 0;

        this.volume = 0.8;
    }

    /**
     * Update the meta data for the current song.
     *
     * @param {number} songIndex Optional param to force set the index of the song.
     */
    updateSong(songIndex) {
        this.previousSong = this.songIndex;
        this.songIndex = songIndex || this.songIndex;
        this.song = songList[this.songIndex];
        const song = this.song;

        audio.src = song.url;
        trackingSlider.value = 0;
        this.updateSongRangeValues();
        songLength.innerHTML = secondsToHms(song.duration);
        trackingSlider.max = song.duration;

        playerArt.src = song.album.art.square;

        document.querySelector(`tr[data-index="${this.previousSong}"]`).classList.remove('playing');
        toggleClasses(document.querySelector(`tr[data-index="${this.songIndex}"]`), 'playing');
    }

    /**
     * Play the audio.
     */
    play() {
        audio.play();
    }

    /**
     * Pause the audio.
     */
    pause() {
        audio.pause();
    }

    /**
     * Seek in the audio, update the time based on range value selected.
     */
    seek() {
        audio.currentTime = Number(trackingSlider.value);
        songCurrentTime.innerHTML = secondsToHms(audio.currentTime);
    }

    /**
     * Update the range values based on the current time in the song.
     */
    updateSongRangeValues() {
        const value = trackingSlider.value / this.song.duration * 100;
        const buffer = 0;

        songCurrentTime.innerHTML = secondsToHms(trackingSlider.value);

        trackingSlider.style.background =
            `linear-gradient(to right, ${colors.aqua[50]} 0%, ${colors.aqua[50]} ${value}%, ${colors.metal[50]} ${value}%, ${colors.metal[50]} ${buffer}%, ${colors.metal[80]} ${buffer}%, ${colors.metal[80]} 100%)`;
    }

    /**
     * Adjust the volume.
     */
    adjustVolume() {
        const {
            value
        } = volumeSlider;
        const buffer = 0;

        audio.volume = value;

        volumeSlider.style.background =
            `linear-gradient(to right, ${colors.aqua[80]} 0%, ${colors.aqua[80]} ${value * 100}%, ${colors.metal[50]} ${value * 100}%, ${colors.metal[50]} ${buffer}%, ${colors.metal[80]} ${buffer}%, ${colors.metal[80]} 100%)`;
    }
}


/**
 * The setup for any set of controls for the player.
 */
class Controls extends Player {
    /**
     * Play or pause the current list item.
     */
    playPause() {
        this.playing = toggleBoolean(this.playing);
        toggleClasses(buttons.playPause, 'on fa-play fa-pause');
        toggleClasses(artPlayer, 'playing');

        const currentClasses = new Set(buttons.playPause.classList);

        if (currentClasses.has('on')) {
            this.play();
        } else {
            this.pause();
        }
    }

    /**
     * Go to the next item in the list.
     */
    next() {
        this.previousSong = this.songIndex;
        let playNext = true;

        toggleClasses(document.querySelector(`tr[data-index="${this.songIndex}"]`), 'playing');

        if (this.shuffle) {
            this.randomIndex++;

            if (this.randomIndex >= this.randomOrder.size) {
                this.randomIndex = 0;

                playNext = this.repeat;
            }

            this.songIndex = Array.from(this.randomOrder)[this.randomIndex];
        } else {
            this.songIndex++;

            if (this.songIndex >= songList.length) {
                this.songIndex = 0;

                playNext = this.repeat;
            }
        }

        this.updateSong();

        if (this.playing) {
            if (playNext) {
                this.play();
            } else {
                this.playPause();
            }
        }
    }

    /**
     * Go to the previous item in the list.
     */
    previous() {
        toggleClasses(document.querySelector(`tr[data-index="${this.songIndex}"]`), 'playing');

        if (this.shuffle) {
            if (this.randomIndex === 0) {
                this.randomIndex = this.randomOrder.size;
            }
            this.randomIndex--;

            this.songIndex = Array.from(this.randomOrder)[this.randomIndex];
        } else {
            if (this.songIndex === 0) {
                this.songIndex = songList.length;
            }
            this.songIndex--;
        }

        this.updateSong();

        if (this.playing) {
            this.play();
        }
    }

    /**
     * Shuffle the list, play in a random order.
     */
    toggleShuffle() {
        this.shuffle = toggleBoolean(this.shuffle);
        toggleClasses(buttons.shuffle, 'on');
        const currentClasses = new Set(buttons.shuffle.classList);

        if (currentClasses.has('on')) {
            this.randomOrder = new Set();
            this.randomIndex = 0;

            let randomIndex = this.songIndex;

            for (let index = 0; index < songList.length; index++) {
                if (window.CP.shouldStopExecution(0)) break;
                // While loop to ensure that the index being added to the random order is unique, else changes the index value
                while (this.randomOrder.has(randomIndex)) {
                    if (window.CP.shouldStopExecution(1)) break;
                    randomIndex = Math.floor(Math.random() * songList.length);
                }
                window.CP.exitedLoop(1);

                this.randomOrder.add(randomIndex);
            }
            window.CP.exitedLoop(0);
        }
    }

    /**
     * Repeat/loop the list that is currently playing.
     */
    toggleRepeat() {
        this.repeat = toggleBoolean(this.repeat);
        toggleClasses(buttons.repeat, 'on');
    }
}



// Instantiate the controls
const controls = new Controls();

// Add event listeners for the buttons
buttons.playPause.addEventListener('click', () => {
    controls.playPause();
});
buttons.next.addEventListener('click', () => {
    controls.next();
});
buttons.previous.addEventListener('click', () => {
    controls.previous();
});
buttons.shuffle.addEventListener('click', () => {
    controls.toggleShuffle();
});
buttons.repeat.addEventListener('click', () => {
    controls.toggleRepeat();
});


audio.onended = () => {
    // Once a song is over play next song.
    controls.next();
};
audio.ontimeupdate = () => {
    trackingSlider.value = audio.currentTime;
    controls.updateSongRangeValues();
};

// Update the range values on change or moving the scrubber.
trackingSlider.addEventListener('change', () => {
    controls.updateSongRangeValues();
    controls.seek();
});
trackingSlider.addEventListener('mousemove', () => {
    controls.updateSongRangeValues();
});

volumeSlider.addEventListener('change', () => {
    controls.adjustVolume();
});
volumeSlider.addEventListener('mousemove', () => {
    controls.adjustVolume();
});

// That's right ... hotkeys!
document.onkeypress = event => {
    switch (event.keyCode) {
        // a - previous
        case 97:
            {
                controls.previous();
                break;
            }
            // d / n - next
        case 100:
        case 110:
            {
                controls.next();
                break;
            }
            // s / p - play / pause
        case 115:
        case 112:
            {
                controls.playPause();
                break;
            }
            // e / r - repeat
        case 101:
        case 114:
            {
                controls.toggleRepeat();
                break;
            }
            // q - shuffle
        case 113:
            {
                controls.toggleShuffle();
                break;
            }
    }

};



/**
 * Build the playlist from the give array of songs.
 */
function buildPlaylist() {
    // Add the songs to the dom
    let html = '';

    songList.forEach((song, index) => {
        html +=
            `
            <tr data-index="${index}">
              <td>${song.title}</td>
              <td>${song.album.title}</td>
              <td>${secondsToHms(song.duration)}</td>
            </tr>

            `;

    });
    playlistBody.innerHTML = html;

    // Update the list items
    listItems = document.querySelectorAll('#playlist tbody');

    // Add event listeners to the list items
    for (const listItem of listItems) {
        listItem.addEventListener('click', event => {
            const songIndex = event.target.parentElement.dataset.index;
            controls.updateSong(songIndex);

            if (controls.playing) {
                controls.play();
            }
        });

        listItem.addEventListener('dblclick', event => {
            event.preventDefault();
            event.stopPropagation();

            if (!controls.playing) {
                controls.playPause();
            }
        });
    }

}


// Initiate the setup.
window.onload = () => {
    buildPlaylist();
    controls.updateSong();
    controls.adjustVolume();
};
//# sourceURL=pen.js
