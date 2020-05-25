const api_url = "http://api.clickcount.cf/api/counts";
const el = document.getElementById('counter-regulator');

document.onload = () => {
    fetch(api_url, { method: 'POST' }).then(h => {
        if (h)
            console.log(h);

        fetch(api_url).then(res => refresh(el.innerHTML = `${res.json().clicks}`));
    });
};

// function gay() {
//     fetch(api_url, { method: 'POST' }).then(h => {
//         if (h)
//             console.log(h);

//         fetch(api_url).then(res => refresh(el.innerHTML = `${res.json().clicks}`));
//     });
// }