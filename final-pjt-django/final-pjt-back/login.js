$(function() {
    $(".input input").focus(function() {
        $(this).parent(".input").each(function() {
            $("label", this).css({
                "line-height": "18px",
                "font-size": "18px",
                "font-weight": "100",
                "top": "0px"
            });
            $(".spin", this).css({
                "width": "100%"
            });
        });
    }).blur(function() {
        $(".spin").css({
            "width": "0px"
        });
        if ($(this).val() == "") {
            $(this).parent(".input").each(function() {
                $("label", this).css({
                    "line-height": "60px",
                    "font-size": "24px",
                    "font-weight": "300",
                    "top": "10px"
                });
            });
        }
    });

    $("#registerButton").click(function() {
        window.location.href = 'register.html'; // 회원가입 페이지 URL로 변경하세요.
    });
});
