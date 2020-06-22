$(function () {
    var $searchBar = $('#searchBar'),
        $searchResult = $('#searchResult'),
        $searchText = $('#searchText'),
        $searchInput = $('#searchInput'),
        $searchClear = $('#searchClear'),
        $searchCancel = $('#searchCancel');
    hideSearchResult();

    function hideSearchResult() {
        $searchResult.hide();
        $searchInput.val('');
    }

    function cancelSearch() {
        hideSearchResult();
        $searchBar.removeClass('weui-search-bar_focusing');
        $searchText.show();
    }

    $searchText.on('click', function () {
        $searchBar.addClass('weui-search-bar_focusing');
        $searchInput.focus();
    });
    $searchInput
        .on('blur', function () {
            if (!this.value.length) cancelSearch();
        })
        .on('input', function () {
            if (this.value.length) {
                sr = $("#searchResult")
                // 先清空结果栏
                sr.empty()
                $.ajax({
                    url: '/api/games/?keyword=' + $searchInput.val(),
                    dataType: 'JSON',
                    method: 'GET',
                    success: function (resp) {
                        if (resp.count > 0) {
                            resp.results.forEach(function (game, index) {
                                temp = '<div class="weui-cell weui-cell_active weui-cell_access">\n' +
                                    '                <div class="weui-cell__bd weui-cell_primary search-item" rel="$1">\n' +
                                    '                    <span class="search-item-cover">\n' +
                                    '                        <img src="$2" alt=""></span>\n' +
                                    '                    <span class="search-item-subject">$3</span>'
                                '                </div>\n' +
                                '            </div>'
                                item = temp.replace('\$1', game.gameId).replace('\$2', game.mp_cover[0]).replace('\$3', game.titleCh)
                                sr.append(item)
                            })
                        }
                    }
                })
                $searchResult.show();
            } else {
                $searchResult.hide();
            }
        })
    ;
    $searchResult.on('click', 'div.search-item', function () {
        var that = this
        gameId = $(that).attr("rel")
        location.href = "/games/info/" + gameId
    })
    $searchClear.on('click', function () {
        hideSearchResult();
        $searchInput.focus();
    });
    $searchCancel.on('click', function () {
        cancelSearch();
        $searchInput.blur();
    });
});