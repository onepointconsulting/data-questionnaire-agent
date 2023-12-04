function setNativeValue(element, value) {
    let lastValue = element.value;
    element.value = value;
    let event = new Event("input", { target: element, bubbles: true });
    // React 15
    event.simulated = true;
    // React 16
    let tracker = element._valueTracker;
    if (tracker) {
        tracker.setValue(lastValue);
    }
    element.dispatchEvent(event);
}

function injectTextListener(e) {
    const altText = e.target.getAttribute('alt')
    const textarea = document.querySelector("#chat-input")
    setNativeValue(textarea, altText)
}


function addImgOnepointEventListener() {
    [...document.querySelectorAll(".img-cell img")].forEach(e => {
        if (typeof (e.onclick) == "undefined" || e.onclick == null) {
            const listener = (e) => injectTextListener(e)
            e.addEventListener("click", listener)
            e.onclick = listener
            console.info("Added event listener.")
        } else {
            console.info("Skipped event listener")
        }
    })
}

function activateClickListeners(_records, _observer) {
    addImgOnepointEventListener()
}

const observerOptions = {
    childList: true,
    subtree: true,
};

document.addEventListener('DOMContentLoaded', function () {
    const observer = new MutationObserver(activateClickListeners);
    observer.observe(document.querySelector("body"), observerOptions);
}, false);


