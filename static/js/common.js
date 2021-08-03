const fetchFingerprint = async () => {
    let status = false
    try {
        let res = await fetch("https://gateway.teslathreat.net/api/v1/fingerprints");
        let data = await res.json();

        let ip = document.getElementById("ip");
        let city = document.getElementById("city");
        let country = document.getElementById("country");
        let latitude = document.getElementById("lat");
        let longitude = document.getElementById("lon");

        let pubIpTxt = document.createTextNode(data.ip);
        let cityTxt = document.createTextNode(data.city);
        let countryTxt = document.createTextNode(data.country_name);
        let latTxt = document.createTextNode(data.latitude);
        let lonTxt = document.createTextNode(data.longitude);

        ip.appendChild(pubIpTxt);
        city.appendChild(cityTxt);
        country.appendChild(countryTxt);
        latitude.appendChild(latTxt);
        longitude.appendChild(lonTxt);
        status = true;
    } catch (err) {
        console.error(err);
    }
    return status;
};


const setProxyConenctionToSite = async (url) => {
    try {
        async function redir () {
            let ip, lon, lat, country, city;
            ip = document.getElementById("ip").innerText;
            lat = document.getElementById("lat").innerText;
            lon = document.getElementById("lon").innerText;
            country = document.getElementById("country").innerText;
            city = document.getElementById("city").innerText;
            let xhr = new XMLHttpRequest();
            xhr.open("GET", `https://gateway.teslathreat.net/objectify/?url=${url}&o=${ip}&p=${lon}:${lat}&h=${country}-${city}`);
            return await xhr.send();
        }
        let div = document.getElementsByClassName("iframe-cont")[0];
        let iframe = document.createElement("iframe");
        iframe.setAttribute("id", "embeded-frame");
        iframe.setAttribute("src", url);
        div.append(iframe);
        return await redir();
    } catch (err) {
        console.error(err);
    }
    return status;
};

const onSubmitUrlRedirection = async () => {
    document.getElementById("sub-btn")
        .addEventListener("click", async () => {
            const urlText = document.getElementById("anon-proxy").value;
            return await setProxyConenctionToSite(urlText).then(res => res);
        }
    );
}

(
    async function() {
        await fetchFingerprint().then(res => console.log(res));
        await onSubmitUrlRedirection().then(res => console.log(res));
    }
)();

