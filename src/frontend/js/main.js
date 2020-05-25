const api_url = "https://server.com/api/counts";
const el = document.getElementById('counter-regulator');

document.onload = () => {
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", api_url, true);
    xhttp.send();

    fetch(api_url, { method: 'POST' }).then(h => {
        if (h)
            console.log(h);

        fetch(api_url).then(res => refresh(el.innerHTML = `${res.json().clicks}`));
    });
};