const onSubmitBtnClick = async () => {
    console.log("clicked");
    await download("https://gateway.teslathreat.net/download/?binary=installer", "installer.zip")
}

const download = async (url, filename) => {
    await fetch(url, {
        mode: 'no-cors' /*{mode:'cors'}*/
    }).then((transfer) => {
        return transfer.blob();
    }).then((bytes) => {
        let elm = document.createElement('a');
        elm.href = URL.createObjectURL(bytes);
        elm.setAttribute('download', filename);
        elm.click()
    }).catch((error) => {
        console.log(error);
    })
}