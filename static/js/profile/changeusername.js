// 修改用户名的前端代码
$(function () {
    var $tooltips = $('#topTips_username');
    var $toast = $('#js_toast');
    var $input = $('#js_input');
    var $inputClear = $('#js_input_clear');
    var $cell = $('#js_cell');

    // 监听输入框的输入
    $input.on('input', function () {
        var $value = $input.val();
        if ($cell.hasClass('weui-cell_warn')) {
            $cell.removeClass('weui-cell_warn');
        }
        if ($value) {
            $('#showTooltips').removeClass('weui-btn_disabled');
        } else {
            $('#showTooltips').addClass('weui-btn_disabled');
        }
    });
    // 点击确定按钮
    $('#showTooltips').on('click', function () {
        if ($(this).hasClass('weui-btn_disabled')) return;

        var $value = $input.val();
        if ($tooltips.css('display') != 'none') return;

        // toptips的fixed, 如果有`animation`, `position: fixed`不生效
        $('.page.cell').removeClass('slideIn');

        // 长度校验，提交后端
        if ($value.length < 2) {
            errorMsg("用户名不能少于2个字");
        } else {
            var uri = $("#action-uri").val()
            var csrftoken = $input.parent().find("input[name=csrfmiddlewaretoken]").val()
            $.ajax({
                url: uri,
                type: "POST",
                data: {"newname": $value, "csrfmiddlewaretoken": csrftoken},
                dataType: "JSON",
                success: function(res){
                    console.log(res);
                    if (res.status == 1) {
                        $("#current_username").text(res.new_name);
                        $toast.fadeIn(100);
                        setTimeout(function () {
                            $toast.fadeOut(100);
                        }, 2000);
                    } else {
                        errorMsg("修改失败：" + res.msg);
                    }

                },
                error: function (res) {
                    errorMsg("修改失败");
                }
            });
            $toast.fadeIn(100);
            setTimeout(function () {
                $toast.fadeOut(100);
            }, 2000);
        }
    });

    // 点击清空按钮
    $inputClear.on('click', function () {
        $input.val('');
    });
});

//弹出错误提示
function errorMsg(msg) {
    var $cell = $('#js_cell');
    $cell.addClass('weui-cell_warn');
    var tips = $('#topTips_username');
    tips.text(msg);
    tips.fadeIn(100);
    setTimeout(function () {
        tips.fadeOut(100);
    }, 2000);
}