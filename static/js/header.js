$(document).ready(() => {

    const checkControl = $('#check-control');
    let isChecked = checkControl.is(':checked');

    const menuMobileLista = $('#menu-mobile__lista');
    const line1 = $('#mobile-line1');
    const line2 = $('#mobile-line2');
    const line3 = $('#mobile-line3');

    checkControl.change(() => {
        isChecked = !isChecked;

        if(isChecked){
            line2.css({'left': '10px', 'transition': '0.1s'}).fadeOut('fast');

            line1.css({'top': '20px','transform': 'rotate(-45deg)' ,'transition': '0.3s'})
        
            line3.css({'top': '12px','transform': 'rotate(45deg)' ,'transition': '0.3s'})
        }else{
            line2.css({'left': '0px', 'transition': '0.7s'}).fadeIn('fast');

            line1.css({'top': '6px','transform': 'rotate(0deg)' ,'transition': '0.3s'})
        
            line3.css({'top': '18px','transform': 'rotate(0deg)' ,'transition': '0.3s'})
        }

        menuMobileLista.slideToggle('fast');

    })

})