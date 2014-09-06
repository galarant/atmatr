add_svg_test = function() {
    svg_test_div = document.getElementById('svg_test');
    svg_test_div.onclick = function() {
        svg_element = this.getElementsByTagName('svg')[0];
        g_element = svg_element.getElementsByTagName('g')[0];
        animation = document.createElementNS("http://www.w3.org/2000/svg",'animateTransform');
        animation.setAttribute('attributeType', 'XML');
        animation.setAttribute('attributeName', 'transform');
        animation.setAttribute('type', 'scale');
        animation.setAttribute('from', '2');
        animation.setAttribute('to', '0');
        animation.setAttribute('dur', '1.5s');
        animation.setAttribute('fill', 'freeze');
        g_element.appendChild(animation);
        animation.beginElement();
    }
}

document.addEventListener("DOMContentLoaded", add_svg_test, false);
