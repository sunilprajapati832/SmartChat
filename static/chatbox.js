(function () {
    const script = document.currentScript;
    const business = script.getAttribute("data-business") || "default";

    const iframe = document.createElement("iframe");
    iframe.src = "http://127.0.0.1:5000/widget?business=" + business;

    iframe.style.position = "fixed";
    iframe.style.bottom = "20px";
    iframe.style.right = "20px";
    iframe.style.width = "360px";
    iframe.style.height = "500px";
    iframe.style.border = "none";
    iframe.style.zIndex = "999999";

    document.body.appendChild(iframe);
})();
