function formatCreditCard() {
    console.log('i m here')
    var x = document.getElementById("cc_no");
    var index = x.value.lastIndexOf(' ');
    var test = x.value.substr(index + 1);
    if (test.length === 4)
         x.value = x.value + ' ';
}