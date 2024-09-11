document.addEventListener('DOMContentLoaded', (event) => {
    // 使 DIV 元素可拖动
    dragElement(document.getElementById("floating-window"));

    // 更新悬浮窗内容
function updateContent() {
    const contentElement = document.getElementById("content");

    // 函数来查找指定标签后的兄弟元素
    function getLabelValue(labelText) {
        const labelElement = Array.from(document.querySelectorAll('span')).find(
            span => span.textContent.trim() === labelText
        );
        return labelElement && labelElement.nextElementSibling ? labelElement.nextElementSibling.textContent.trim() : null;
    }

    // 获取 car_brand_name、car_series_name 和 car_type_name
    const carBrandName = getLabelValue('品牌');
    const carSeriesName = getLabelValue('车系');
    const carTypeName = getLabelValue('车型');

    // 检查是否都成功获取了值
    if (carBrandName && carSeriesName && carTypeName) {
        contentElement.textContent = '加载中...';

        // 构造 API 查询内容
        const queryContent = `你要扮演的角色是一位拥有多年经验的专业车评人，对我给出的车辆进行专业的评价，我想要你评价的车是：${carBrandName} ${carSeriesName} ${carTypeName}，请精炼简短的评价，字数在二百字左右`;

        // 调用 API 获取响应
        fetchChatGPTResponse(queryContent, carBrandName, carSeriesName, carTypeName);
    } else {
        contentElement.textContent = '未找到车型信息元素';
    }
}

function fetchChatGPTResponse(queryContent, carBrandName, carSeriesName, carTypeName) {
    const apiKey = 'sk-aZmXPBcVJEdiF7me18C149F331B9450290Ad0bDcE7F963C0';  // 替换为你的 API 密钥
    const apiUrl = 'https://xiaoai.plus/v1/chat/completions';

    const requestBody = {
        model: 'gpt-3.5-turbo',
        messages: [
            { role: 'user', content: queryContent }
        ]
    };

    // 发起 API 请求
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
        // 显示 API 响应内容
        if (data && data.choices && data.choices.length > 0) {
            contentElement.innerHTML = `<p><strong>AI分析：</strong> ${data.choices[0].message.content}</p>`;
        } else {
            contentElement.textContent = '未能获取响应';
        }
    })
    .catch(error => {
        const contentElement = document.getElementById("content");
        contentElement.textContent = '错误：' + error.message;
    });
}

// 初始调用更新内容
updateContent();


    // 使悬浮窗可拖动
    function dragElement(elmnt) {
        let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

        if (document.getElementById(elmnt.id + "header")) {
            // 如果存在 header，从 header 移动 DIV
            document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
        } else {
            // 否则，从 DIV 内任意位置移动 DIV
            elmnt.onmousedown = dragMouseDown;
        }

        function dragMouseDown(e) {
            e = e || window.event;
            e.preventDefault();
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            document.onmousemove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
            elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
        }

        function closeDragElement() {
            document.onmouseup = null;
            document.onmousemove = null;
        }
    }
});
