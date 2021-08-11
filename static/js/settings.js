var basket = document.getElementById("basket");
var user = document.getElementById("user");

var cross = document.getElementById("cross");

var ul = document.getElementById("ul");
var li = document.getElementById("sp");


ul.style.display = "none";
document.getElementById("usermini").style.display = "none";

basket.addEventListener("click", function() {

    document.getElementById("basketin").style.right = "0";
});

cross.addEventListener("click", function() {

    document.getElementById("basketin").style.right = "-450px";
});


user.addEventListener("click", function() {

    if (document.getElementById("usermini").style.display == "none") { document.getElementById("usermini").style.display = "block"; } else { document.getElementById("usermini").style.display = "none"; }
});

li.addEventListener("click", function fclick() {

    if (ul.style.display == "none") { ul.style.display = "block"; } else { ul.style.display = "none"; }
});

/* width */
const delItem = document.getElementsByClassName("delItem");

for (d of delItem) {
    d.addEventListener('click', function() {

        let proNum = $(this)[0].attributes[2].nodeValue;

        //window.location.href="/card/update/"+proNum;
        $.ajax({
            url: "/card/delete/" + proNum,
            method: "GET",
            dataType: 'json',
            success: function(data) {

                Swal.fire({ icon: 'success', title: 'Sepetten Çıkarıldı', showConfirmButton: false, timer: 1500 });
                setTimeout(function() { window.location.reload(); }, 2000);


            }
        });
    });

}





var hmbgr = document.getElementById("hmbgr");

hmbgr.addEventListener("click", function() {

    if (window.screen.width < 600) {
        document.getElementById('nav-inner').style.left = '0';

    }
});

var close = document.getElementById("close");

close.addEventListener("click", function() {

    if (window.screen.width < 600) {
        document.getElementById('nav-inner').style.left = '-450px';

    }
});


for (i of document.getElementsByClassName("tempalt")) {
    i.style.height = "45px";
}

try {
    listener();

    function listener() { document.getElementById("tempsss").addEventListener("click", clp) }

    function clp(e) {

        if (e.target.classList.contains("fs")) {

            if (e.target.parentElement.style.height == "45px") {
                e.target.parentElement.style.height = "188px";
            } else { e.target.parentElement.style.height = "45px"; }

        }
    }
} catch (e) {

}

try {



    const thresh = document.getElementsByClassName("cart-tresh");

    for (t of thresh) {
        t.addEventListener('click', function() {

            let proNum = $(this)[0].attributes[1].nodeValue;


            //window.location.href="/card/update/"+proNum;
            $.ajax({
                url: "/card/delete/" + proNum,
                method: "GET",
                dataType: 'json',
                success: function(data) {

                    Swal.fire({ icon: 'success', title: 'Sepetten Çıkarıldı', showConfirmButton: false, timer: 1500 });
                    setTimeout(function() { window.location.reload(); }, 2000);


                }
            });
        });

    }
} catch (error) {

}
try {
    function showh() {
        if (document.getElementById("showh").style.display == "none") {
            document.getElementById("showh").style.display = "block";
        }

    }


} catch (error) {

}
try {
    var login = document.getElementById("login");
    var register = document.getElementById("register");

    login.addEventListener("click", function() { window.location.href = "https://www.oyunganimeti.com/login/"; });
    register.addEventListener("click", function() { window.location.href = "https://www.oyunganimeti.com/register/"; });
} catch (error) {

}

try {
    const buyitem = document.getElementsByClassName("buy-item");

    for (b of buyitem) {
        b.addEventListener('click', function() {

            let proNum = $(this)[0].attributes[1].nodeValue;
            //window.location.href="/card/update/"+proNum;
            $.ajax({
                url: "/card/update/" + proNum,
                method: "GET",
                dataType: 'json',
                success: function(data) {

                    Swal.fire({ icon: 'success', title: 'Sepete Eklendi', showConfirmButton: false, timer: 1500 });
                    setTimeout(function() { window.location.reload(); }, 2000);


                }
            });
        });

    }
} catch (error) {

}
try {
    const addBasketBtn = document.getElementsByClassName("add-basket-btn");

    for (a of addBasketBtn) {
        a.addEventListener('click', function() {

            let proNum = $(this)[0].attributes[1].nodeValue;
            //window.location.href="/card/update/"+proNum;
            $.ajax({
                url: "/card/update/" + proNum,
                method: "GET",
                dataType: 'json',
                success: function(data) {

                    Swal.fire({ icon: 'success', title: 'Sepete Eklendi', showConfirmButton: false, timer: 1500 });
                    setTimeout(function() { window.location.reload(); }, 2000);


                }
            });
        });

    }
} catch (error) {

}