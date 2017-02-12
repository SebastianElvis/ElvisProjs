function get_records_info(page, num, type, sort){
    var params_without_page = 'num=' + num + '&'
            + 'type=' + type + '&'
            + 'sort=' + sort + '&'
            + 'page=';
    var url = '/getrecords?' + params_without_page + page;
    $.getJSON(url, function(data){
        for(i=0;i<data.records_list.length;i++){
            var td_poster = '<td>' + data.records_list[i].poster +  '</td>';
            var td_content = '<td>' + data.records_list[i].content +  '</td>';
            var td_type = '<td>' + data.records_list[i].type +  '</td>';
            var td_time = '<td>' + data.records_list[i].time +  '</td>';
            var tr = '<tr>' + td_poster + td_content + td_type + td_time + '</tr>';
            $('#tb').append(tr);
        }

        var page_count = Math.ceil(data.count/num);
        page_nav(page, page_count, params_without_page);
    });
}

function page_nav(page, page_count, params_without_page){
    var url_without_page = '/news?' + params_without_page;
    var cur_page_elem = $('#cur_page');
    var i = 0;
    var before_li = '', after_li = '';

    //prev and next
    if(page == 1){
        $('#nav_prev').addClass('disabled');
    } else {
        $('#nav_prev > a').attr('href', url_without_page + (page-1));
    }
    if(page == page_count){
        $('#nav_next').addClass('disabled');
    } else {
        $('#nav_next > a').attr('href', url_without_page + (page+1));
    }

    // before cur_page
    for(i=(page-1);i>0&&(page-i<5);i--){
        before_li = '<li><a href="' + url_without_page + i + '">' + i + '</a></li>' + before_li;
    }
    if(i > 0){
        before_li = '<li class="disabled"><a>...</a></li>' + before_li;
        before_li = '<li><a href="' + url_without_page + 1 + '">' + 1 + '</a></li>' + before_li;
    }
    cur_page_elem.before(before_li);

    // after cur_page
    for(i=(page+1);i<page_count&&(i-page)<5;i++){
        after_li += '<li><a href="' + url_without_page + i + '">' + i + '</a></li>';
    }
    if(i <page_count){
        after_li += '<li class="disabled"><a>...</a></li>';
        after_li += '<li><a href="' + url_without_page + page_count + '">' + page_count + '</a></li>';
    }
    cur_page_elem.after(after_li);
}