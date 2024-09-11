document.addEventListener('DOMContentLoaded', (event) => {
    // Make the DIV element draggable
    dragElement(document.getElementById("floating-window"));

    // Function to update the content of the floating window
    function updateContent() {
        const contentElement = document.getElementById("content");
        const carTypeNameElements = document.querySelectorAll('td.col5 a');

        // Check if car_type_name elements exist
        if (carTypeNameElements.length > 0) {
            const carTypeName = carTypeNameElements[0].textContent;
            contentElement.textContent = 'Loading...';

            // Call the API with car_type_name
            fetchChatGPTResponse(carTypeName);
        } else {
            contentElement.textContent = 'Car type name element not found';
        }
    }

    // Function to fetch the response from ChatGPT API
    function fetchChatGPTResponse(carTypeName) {
        const apiKey = 'sk-aZmXPBcVJEdiF7me18C149F331B9450290Ad0bDcE7F963C0';  // Replace with your API key
        const apiUrl = 'https://xiaoai.plus/v1/chat/completions';

        const requestBody = {
            model: 'gpt-3.5-turbo',
            messages: [
                { role: 'user', content:   '你要扮演的角色是一位拥有多年经验的专业车评人，对我给出的车辆进行专业的评价，我想要你评价的车是：'+ carTypeName +'，请精炼简短的评价，字数在二百字左右'}
            ]
        };

        // Make the API request
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + apiKey
            },
            body: JSON.stringify(requestBody)
        })
        .then(response => response.json())
        .then(data => {
            const contentElement = document.getElementById("content");
            // Check if we got a valid response
            if (data && data.choices && data.choices.length > 0) {
                contentElement.textContent = data.choices[0].message.content;
            } else {
                contentElement.textContent = 'Failed to fetch response';
            }
        })
        .catch(error => {
            const contentElement = document.getElementById("content");
            contentElement.textContent = 'Error: ' + error.message;
        });
    }

    // Initial call to update content
    updateContent();

    // Function to make the floating window draggable
    function dragElement(elmnt) {
        let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

        if (document.getElementById(elmnt.id + "header")) {
            // If a header exists, move the DIV from the header
            document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
        } else {
            // Otherwise, move the DIV from anywhere inside the DIV
            elmnt.onmousedown = dragMouseDown;
        }

        function dragMouseDown(e) {
            e = e || window.event;
            e.preventDefault();
            // Get the mouse cursor position at startup
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            // Call a function whenever the cursor moves
            document.onmousemove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            // Calculate the new cursor position
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            // Set the element's new position
            elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
            elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
        }

        function closeDragElement() {
            // Stop moving when mouse button is released
            document.onmouseup = null;
            document.onmousemove = null;
        }
    }
});
