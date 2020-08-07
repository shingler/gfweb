// 获取上传token
// console.log(oss_token);
// console.log(current_uid);

// 设置上传参数
function set_upload_param(up) {
    // 获取上传签名
    obj = oss_token;
    host = obj['host'];
    policyBase64 = obj['policy'];
    accessid = obj['accessid'];
    signature = obj['signature'];
    expire = parseInt(obj['expire']);
    callbackbody = obj['callback'];
    key = obj['dir'] + "/" + current_uid;
    timestamp = Date.parse(new Date()) / 1000;

    new_multipart_params = {
        'key': key,
        'policy': policyBase64,
        'OSSAccessKeyId': accessid,
        'success_action_status': '200', //让服务端返回200,不然，默认会返回204
        // 'callback' : callbackbody,
        'signature': signature,
    };
    console.log(new_multipart_params);
    up.setOption({
        'url': host,
        'multipart_params': new_multipart_params
    });

    up.start();
}

// 获得头像路径
function get_avatar_path() {
    obj = oss_token;
    host = obj['host'];
    key = obj['dir'] + "/" + current_uid;
    timestamp = Date.parse(new Date()) / 1000;
    return host + "/" + key + "?v=" + timestamp;
}

// 实例化上传组件
var uploader = new plupload.Uploader({
    runtimes : 'html5,flash,silverlight,html4',
	browse_button : 'selectfiles',
	flash_swf_url : 'lib/plupload-2.1.2/js/Moxie.swf',
	silverlight_xap_url : 'lib/plupload-2.1.2/js/Moxie.xap',
    url : 'http://oss.aliyuncs.com',

    filters: {
        mime_types: [ //只允许上传图片
            {title: "Image files", extensions: "jpg,jpeg,gif,png"},
        ],
        max_file_size: '5mb', //最大只能上传5mb的文件
        prevent_duplicates: true //不允许选取重复文件
    },
});
uploader.init();

/** 绑定方法 **/
// 添加文件
uploader.bind("FilesAdded", function (up, files) {
    set_upload_param(up);
    return false;
});
//上传成功
uploader.bind("FileUploaded", function (up, file, info) {
    if (info.status == 200) {
        // 将新头像地址保存到数据库
        var csrftoken = $("#selectfiles").parent().find("input[name=csrfmiddlewaretoken]").val()
        var post_data = {
            "avatar_path": get_avatar_path(),
            "csrfmiddlewaretoken": csrftoken,
        };
        $.ajax({
            url: "/auth/changeavatar",
            type: "post",
            data: post_data,
            dataType: "json",
            success: function (res) {
                $("#current_avatar").attr("src", res.data.avatar);
                // 成功提示
                var toast = $("#js_toast");
                toast.fadeIn(100);
                setTimeout(function () {
                    toast.fadeOut(100);
                    location.reload();
                }, 2000);
            },
            error: function (res) {
                errorMsg(res.msg);
            }
        });
    } else {
        errorMsg("上传失败");
    }
});
//报错
uploader.bind("Error", function (up, err) {
    if (err.code == -600) {
        errorMsg("选择的文件太大了, 最多可以上传5MB");
    } else if (err.code == -601) {
        errorMsg("选择的文件后缀不对,可以根据应用情况，在upload.js进行设置可允许的上传文件类型");
    } else if (err.code == -602) {
        errorMsg("这个文件已经上传过一遍了");
    } else {
        errorMsg("出错了！" + err.response);
    }
});
//弹出错误提示
function errorMsg(msg) {
    var tips = $('#topTips_avatar');
    tips.text(msg);
    tips.fadeIn(100);
    setTimeout(function () {
        tips.fadeOut(100);
    }, 2000);
}