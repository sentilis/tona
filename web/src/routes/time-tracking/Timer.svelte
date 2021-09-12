<script>
    import { API_URL } from "../../constants";
    import { DateToUTC, URLJoin } from "../../utils";
    import { formatDuration } from "./index";
    export let entryName = "";
    export let entryResId = 0;
    export let entryResModel = "";

    let entryDuration = "00:00:00";
    let entryStart = null;
    let entryRunning = false;
    let playId = null;

    let Current = () => {
        return new Promise(function (resolve, reject) {
            try {
                fetch(
                    URLJoin(API_URL, `/api/v1/time-tracking/entries/current`),
                    {
                        method: "get",
                        headers: {
                            Accept: "application/json",
                            "Content-Type": "application/json",
                        },
                    }
                )
                    .then(async (res) => {
                        if (res.status == 200) {
                            let data = await res.json();
                            data = data["payload"];
                            entryName = data["name"];
                            Start(data["start"]);
                            return resolve(data);
                        }
                    })
                    .catch((err) => {
                        return reject(err);
                    });
            } catch (error) {}
        });
    };

    let Start = (start = Date.now()) => {
        entryStart = start;

        let data = { name: entryName };

        if (entryResId > 0 && entryResModel.length > 0) {
            data["res_id"] = entryResId;
            data["res_model"] = entryResModel;
        }

        if (typeof start === "string") {
            entryStart = Date.parse(start);
            Play();
            return;
        }
        if (
            (entryResId > 0 && entryResModel.length > 0) ||
            entryName.length > 0
        ) {
            data["start"] = DateToUTC(new Date(start));
            fetch(URLJoin(API_URL, `/api/v1/time-tracking/entries/start`), {
                method: "post",
                body: JSON.stringify(data),
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
            })
                .then((res) => {
                    if (res.status == 201) {
                        //let data = res.json();
                        Play();
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
        }
    };

    let Stop = () => {
        let data = { id: 0, stop: DateToUTC(new Date()) };
        fetch(URLJoin(API_URL, `/api/v1/time-tracking/entries/stop`), {
            method: "post",
            body: JSON.stringify(data),
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
        })
            .then((res) => {
                if (res.status == 202) {
                    //let data = res.json();
                    clearInterval(playId);
                    entryStart = null;
                    playId = null;
                    entryRunning = false;
                    entryName = "";
                    entryDuration = "00:00:00";
                }
            })
            .catch((err) => {
                console.log(err);
            });
    };

    let Play = () => {
        playId = setInterval(function () {
            var delta = Date.now() - entryStart;
            var seconds = Math.floor(delta / 1000);
            entryDuration = formatDuration(seconds);
            entryRunning = true;
        }, 1000);
    };

    let ToggleStartStop = () => {
        if (entryRunning) {
            Stop();
        } else {
            Start();
        }
    };
</script>

{#await Current() then _}
    <span />
{/await}

<div class="field has-addons">
    <p class="control">
        <a class="button">{entryDuration}</a>
    </p>
    <p class="control is-expanded">
        <input
            id="time-entry-name"
            bind:value={entryName}
            class="input"
            type="text"
            placeholder="What are you working on?"
        />
    </p>
    <p class="control" on:click={ToggleStartStop}>
        <a
            class="button is-primary {entryRunning ? 'is-hidden' : ''}"
            title="Start time entry"
        >
            <span class="icon">
                <i class="fas fa-clock" />
            </span>
        </a>
        <a
            class="button is-danger {entryRunning ? '' : 'is-hidden'}"
            title="Stop time entry"
        >
            <span class="icon">
                <i class="fas fa-stop" />
            </span>
        </a>
    </p>
</div>
