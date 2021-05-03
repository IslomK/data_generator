$((setInterval(function () {
    $('.dynamic-form').each(function () {
        var form = $(this).find("select");
        form.on("change", function () {
            var value = $(this).val();

            var max_int = $(this).closest('tr').find(".max-int");
            var text_len = $(this).closest('tr').find(".text_len");
            var date_range = $(this).closest('tr').find(".date_between");

            if (value === 'integer') {
                text_len.css("display", "none");
                date_range.css("display", "none")
                max_int.css("display", "block");
            } else if (value === 'text') {
                text_len.css("display", "block")
                date_range.css("display", "none")
                max_int.css("display", "none")
            } else if (value === 'date') {
                max_int.css("display", "none")
                date_range.css("display", "block")
                text_len.css("display", "none")
            } else {
                max_int.css("display", "none")
                date_range.css("display", "none")
                text_len.css("display", "none")
            }
        })
    })
}, 2000)))