(function () {
  const businessKey =
    window.ChatBoxID || "default_business";

  const iframe = document.createElement("iframe");

  iframe.src =
    "https://smartchat.onrender.com/widget?business=" +
    businessKey;

  iframe.style.position = "fixed";
  iframe.style.bottom = "20px";
  iframe.style.right = "20px";
  iframe.style.width = "360px";
  iframe.style.height = "520px";
  iframe.style.border = "none";
  iframe.style.zIndex = "9999";
  iframe.style.borderRadius = "12px";
  iframe.style.boxShadow = "0 10px 30px rgba(0,0,0,0.2)";

  document.body.appendChild(iframe);
})();
