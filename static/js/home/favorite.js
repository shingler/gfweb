// 鼠标经过
$(".favorite-btn span").mouseover(function(){
    if ($(this).hasClass("glyphicon-star")) {
        $(this).removeClass("glyphicon-star");
        $(this).addClass("glyphicon-star-empty");
        $(this).attr("title", "取消收藏");
    } else if ($(this).hasClass("glyphicon-star-empty")) {
        $(this).removeClass("glyphicon-star-empty");
        $(this).addClass("glyphicon-star");
        $(this).attr("title", "添加收藏");
    }
});
// 鼠标离开
$(".favorite-btn span").mouseout(function(){
    if ($(this).hasClass("glyphicon-star")) {
        $(this).removeClass("glyphicon-star");
        $(this).addClass("glyphicon-star-empty");
        $(this).attr("title", "取消收藏");
    } else if ($(this).hasClass("glyphicon-star-empty")) {
        $(this).removeClass("glyphicon-star-empty");
        $(this).addClass("glyphicon-star");
        $(this).attr("title", "添加收藏");
    }
});