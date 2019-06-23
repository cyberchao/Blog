$(function(){
    console.log($(".alert-primary").length);
    if($(".alert-primary").length){
        window.setTimeout(function(){
        $('.alert-primary').alert('close');
    },1500);
    }
    let heigh=document.documentElement.scrollHeight;
    console.log(heigh);
    $("body").height(heigh)
})
