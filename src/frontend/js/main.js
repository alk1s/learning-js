const api_url = "https://api.clickcount.cf/api/counts";

function autistic() {
    fetch(api_url, { method: 'POST' }).then(async res => {
        if (res.status != 204)
            return console.log(await res.json());

        fetch(api_url).then(async res => {
            if (res.status != 200)
                return console.log(await res.json());

            document.getElementById("counter-regulator").innerHTML = `${(await res.json()).clicks} clicks`;
        });
    });
}