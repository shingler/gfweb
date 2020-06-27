// 页面加载初始化
$(function () {
    $('[data-toggle="tooltip"]').tooltip();
})
// 删除弹窗
$("#unlinkModal").on("show.bs.modal", function(e) {
    var url = $(e.relatedTarget).attr("data-url");
    var gid = $(e.relatedTarget).parents("li").attr("data-gid");
    $(this).attr("data-url", url);
    $(this).attr("data-gid", gid);
});

// 执行删除
$("#modal-confirm").on('click', function(e) {
    var url = $(this).parents("#unlinkModal").attr("data-url");
    var gid = $(this).parents("#unlinkModal").attr("data-gid");
    $.get(url, function(data, status) {
        if (data.status == 1) {
            $("li[data-gid="+gid+"]").remove();
            $("div.alert p").text(data.msg);
            $("div.alert").removeClass("alert-warning");
            $("div.alert").addClass("alert-success");
        } else {
            $("div.alert").removeClass("alert-success");
            $("div.alert").addClass("alert-warning");
            $("div.alert p").text(data.msg);
        }
    });
    $("div.alert").removeClass("hidden");
    $("#unlinkModal").modal('hide');
    // 2秒后隐藏警告框
    setTimeout(function(){
        $("div.alert").addClass("hidden");
    }, 2000);
});

// 执行图片转存
$(".save-to-oss").on("click", function (e) {
    var url = $(this).attr("data-url");
    var gid = $(this).attr("game_id");
    var csrf = $(this).attr("data-csrf");
    var btn = $(this).button('loading');
    var parent = $(this).parents("li");
    $(btn).removeClass("glyphicon-picture");
    $(btn).addClass("glyphicon-hourglass")

    //转存请求
    $.ajax({
        url: url,
        type: "GET",
        dataType: "JSON",
        success: function (res) {
            if (res.status == 1) {
                // 按钮状态变化
                btn.button("complete");
                $(btn).removeClass("glyphicon-hourglass");
                $(btn).addClass("glyphicon-ok");
                $(btn).removeClass("btn-info");
                $(btn).removeClass("btn-danger");
                $(btn).addClass("btn-success");
                // 修改转存标签
                var save_label = $(parent).find("span.cover-has-save");
                $(save_label).removeClass("label-danger");
                $(save_label).addClass("label-success");
                $(save_label).removeClass("glyphicon-remove");
                $(save_label).addClass("glyphicon-ok");
                $(save_label).text(" 已转存");
            } else {
                // 按钮状态恢复
                btn.button("reset");
                $(btn).removeClass("glyphicon-hourglass");
                $(btn).addClass("glyphicon-refresh");
                $(btn).removeClass("btn-info");
                $(btn).addClass("btn-danger");
            }
        },
        fail: function (res) {
            // 按钮状态恢复
            btn.button("reset");
            $(btn).removeClass("glyphicon-hourglass");
            $(btn).addClass("glyphicon-refresh");
            $(btn).removeClass("btn-info");
            $(btn).addClass("btn-danger");
        },
        error: function (res) {
            // 按钮状态恢复
            btn.button("reset");
            $(btn).removeClass("glyphicon-hourglass");
            $(btn).addClass("glyphicon-refresh");
            $(btn).removeClass("btn-info");
            $(btn).addClass("btn-danger");
        }
    })
    // $btn.button("reset");

})