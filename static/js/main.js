
// debounce関数
function debounce(func, wait) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            func.apply(context, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}


// menu
$(window).on("load resize", debounce(function() {

			//小さな端末用
			if(window.innerWidth < 900) {	// ※ここがブレイクポイント指定箇所です
				$('body').addClass('s').removeClass('p');
				$('#menubar').addClass('d-n').removeClass('d-b');
				$('#menubar_hdr').removeClass('d-n ham').addClass('d-b');
				
			//大きな端末用
			} else {
				$('body').addClass('p').removeClass('s');
				$('#menubar').addClass('d-b').removeClass('d-n');
				$('#menubar_hdr').removeClass('d-b').addClass('d-n');
			}

}, 5));


//ハンバーガーメニューをクリックした際の処理
$(function() {
	$('#menubar_hdr').click(function() {
		$(this).toggleClass('ham');

			if($(this).hasClass('ham')) {
				$('#menubar').addClass('d-b');
			} else {
				$('#menubar').removeClass('d-b');
			}

	});
});


// 同一ページへのリンクの場合に開閉メニューを閉じる処理
$(function() {
	$('#menubar a[href^="#"]').click(function() {
		$('#menubar').removeClass('d-b');
		$('#menubar_hdr').removeClass('ham');
	});
});


//ドロップダウンの親liタグ
$(function() {
    $('#menubar a[href=""]').click(function() {
		return false;
    });
});


//ドロップダウンメニューの処理
$(function() {

	$('#menubar li:has(ul)').addClass('ddmenu_parent');
	$('.ddmenu_parent > a').addClass('ddmenu');

		//タッチデバイス用
		$('.ddmenu').on('touchstart', function() {
			$(this).next('ul').stop().slideToggle();
			$('.ddmenu').not(this).next('ul').slideUp();
			return false;
		});

		//PC用
		$('.ddmenu_parent').hover(function() {
			$(this).children('ul').stop().slideDown();
		}, function() {
			$(this).children('ul').stop().slideUp();
		});

});


//ドロップダウンをページ内リンクで使った場合に、ドロップダウンを閉じる。
$(function() {
	$('.ddmenu_parent ul a').click(function() {
		$('.ddmenu_parent ul').slideUp();
	});
});


// スムーススクロール（※headerがfixedの場合、かつheaderのmarginを考慮したい場合）
$(window).on("load resize", debounce(function() {
	var headerHeight = $('header').outerHeight();
	var headerMargin = parseInt($('header').css("margin-top"));
	var totalHeaderHeight = headerHeight + headerMargin;
	var hash = location.hash;
	if(hash) {
		$('body,html').scrollTop(0);
		setTimeout(function() {
			var target = $(hash);
			var scroll = target.offset().top - totalHeaderHeight;
			$('body,html').animate({scrollTop:scroll},500);
		}, 5);
	}
	$('a[href^="#"]').click(function() {
		var href = $(this).attr('href');
		var target = href == '#' ? 0 : $(href).offset().top - totalHeaderHeight;
		$('body,html').animate({scrollTop:target},500);
		return false;
	});
}, 5));


//pagetop
$(function() {
    var scroll = $('.pagetop');
    var scrollShow = $('.pagetop-show');
        $(scroll).hide();
        $(window).scroll(function() {
            if($(this).scrollTop() >= 300) {
                $(scroll).fadeIn().addClass(scrollShow);
            } else {
                $(scroll).fadeOut().removeClass(scrollShow);
            }
        });
});


// 汎用開閉処理
$(function() {
	$('.openclose').next().hide();
	$('.openclose').click(function() {
		$(this).next().slideToggle();
		$('.openclose').not(this).next().slideUp();
	});
});
