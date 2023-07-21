// 提取出一个函数用于删除指定类名的元素
function removeElementsByClass(className) {
    let elements = document.querySelectorAll(className);
    for(let i = 0; i < elements.length; i++){
        elements[i].parentNode.removeChild(elements[i]);
    }
}

// 删除所有class="colorDeep marginRight40 fl"的span
removeElementsByClass('span.colorDeep.marginRight40.fl');

// 删除所有class="colorShallow"的span
removeElementsByClass('span.colorShallow');

// 获取所有class含有questionLi的元素中的innerText
let textContents = [];
let elements = document.querySelectorAll('.questionLi');
for(let i = 0; i < elements.length; i++){
    let text = elements[i].innerText.trim(); // trim each line
    textContents.push(text.replace(/(\n\s*){2,}/g, '\n'));
}

// Join the text contents with two newlines
let joinedText = textContents.join('\n\n');

// 输出成一个文本文件并下载
let blob = new Blob([joinedText], {type: "text/plain;charset=utf-8"});
let url = URL.createObjectURL(blob);
let link = document.createElement('a');
link.href = url;
link.download = document.querySelector(".mark_title").innerText+".txt";
document.body.appendChild(link);
link.click();
document.body.removeChild(link);