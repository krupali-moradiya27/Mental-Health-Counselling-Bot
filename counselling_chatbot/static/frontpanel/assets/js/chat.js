document.getElementById("sendMessage").addEventListener("click", function () {
    let inputField = document.querySelector('[data-kt-element="input"]');
    let userMessage = inputField.value.trim();
    
    if (userMessage !== "") {
        let chatBody = document.getElementById("kt_chat_messenger_body");

        // Add user message to chat
        let userMessageHtml = `<div class="message user"><p><strong>You:</strong> ${userMessage}</p></div>`;
        chatBody.innerHTML += userMessageHtml;

        // Send request to Django backend
        fetch("/chat-response/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: "message=" + encodeURIComponent(userMessage)
        })
        .then(response => response.json())
        .then(data => {
            // Add bot response to chat
            let botMessageHtml = `<div class="message bot"><p><strong>Bot:</strong> ${data.response}</p></div>`;
            chatBody.innerHTML += botMessageHtml;

            // Clear input field
            inputField.value = "";
        })
        .catch(error => console.error("Error:", error));
    }
});

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        cookies.forEach(cookie => {
            let [cookieName, cookieVal] = cookie.trim().split("=");
            if (cookieName === name) {
                cookieValue = decodeURIComponent(cookieVal);
            }
        });
    }
    return cookieValue;
}
