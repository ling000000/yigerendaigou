var Product = {
    snatchData: {},
    Init: function () {
        this.snatchData = prodcutMsg;
        //this.goodsList.init();
        this.skuGroup.init();
        //this.method();
        //this.Freight();
    },
    skuGroup: {
        skuData: {},
        skuType: function (sku) {

            for (var i = 0; i < sku.length; i++) {
                this.skuData[sku[i].TypeName] ? this.skuData[sku[i].TypeName].push(sku[i]) : this.skuData[sku[i].TypeName] = [sku[i]];
            };
            return false;
        },
        init: function () {
            var sku = Product.snatchData.Skus;

            this._BindAddQuantityEvent();
            this._BindSubQuantityEvent();
            this._BindQuantityEvent();
            //this.addInfo();
            if (!sku || sku == "null" || sku.length == 0) { return false; };
            this.isSku();
            this.skuType(sku);
            //this.addSku();
            this.addmethod();
            this.skuOne();
            errorSku = this.errSku;
            this.skuAddHui(true);
            this.removeSkuid(); //删除所有和无用skuid相关联的组合id
        },
        skuOne: function () {
            $('.left .img_box').each(function (i, t) {
                if ($('a', t).length == 1) {
                    Product.skuGroup.liclick($('a', t), true);
                }
            });
            return false;
        },
        _BindAddQuantityEvent: function () {
            // $("#goodsInfoDiv").find("[data-name=addQuantity]").click(function () {
            $("#addQuantity").click(function () {
                if (Product.skuGroup._CheckQuantity()) {
                    $("#quantity").val(parseInt($("#quantity").val()) + 1);
                }
            });
        },
        _BindSubQuantityEvent: function () {
            $("#subQuantity").click(function () {
                if (Product.skuGroup._CheckQuantity() && $("#quantity").val() != "1") {
                    $("#quantity").val(parseInt($("#quantity").val()) - 1);
                }
            });
        },
        _BindQuantityEvent: function () {
            $("#quantity").change(function () {
                Product.skuGroup._CheckQuantity();
            }).keyup(function () {
                Product.skuGroup._CheckQuantity();
            });
        },
        _CheckQuantity: function () {
            var value = $("#quantity").val();
            var reg = /^[1-9][0-9]*$/;

            if (reg.test(value) == false) {
                $("#quantity").addClass("input_error");
                //$("#quantity").val(1);
                return false;
            } else {
                $("#quantity").removeClass("input_error");
                return true;
            }
        },
        _CheckPriceRMB: function () {
            var value = $("#buyfreight").val();

            var reg = /^([1-9][0-9]*)$|^([0]|[1-9][0-9]*)(.[0-9]{1,2})+$/;

            if (reg.test(value) == false) {
                $("#buyfreight").addClass("input_error");
                return false;
            } else {
                $("#buyfreight").removeClass("input_error");
                return true;
            }
        },
        skuAddHui: function (isOne) {//第一次检测
            var onSku = [], errSku = this.errSku;
            if (errSku.length == 0 || $('.left .img_box').length == 1) return false;
            $('.left .img_box').each(function (i, t) {
                if ($('a.active', t).length > 0) onSku.push($('a.active', t).attr('data-skuid'));
            });
            var id = this.examineId(onSku);
            this.removeSku = isOne ? id : [];
            $('.left .img_box a').each(function (i, t) {

                if ($(t).hasClass('active ico_dg')) return;
                var skuId = $(t).attr('data-skuid');
                if (!isOne) {
                    $.inArray(skuId, id) >= 0 ? $(t).addClass('no_active').children().addClass("mark") : $(t).removeClass('no_active').children().removeClass("mark");
                } else {
                    $.inArray(skuId, id) >= 0 ? $(t).remove() : '';
                }
            });
            return false;
        },
        errSku: [],
        okSku: [],
        isSku: function () {//把sku组合可以用的和不可以的分类
            var com = Product.snatchData.SkuCombinations,
                errSku = [];
            if (!com || com.length == 0) return false;
            for (var i = 0; i < com.length; i++) {
                com[i].Quantity <= 0 ? this.errSku.push(com[i]) : this.okSku.push(com[i])
            };
            return false;
        },
        removeSkuid: function () {
            var removeSku = this.removeSku,
                 errSku = this.errSku,
                 newErrSku = [];
            for (var i = 0, len = errSku.length; i < len; i++) {
                if (!$.inArray(errSku[i], removeSku) >= 0) {
                    newErrSku.push(errSku[i]);
                }
            }
            this.errSku = newErrSku;
        },
        examineId: function (onSku) {//查找未成功id
            var errsku = this.errSku,
                okSku = this.okSku,
                query = this.query;
            var errorZ = [],
                typeData = this.skuData; //分类后的sku
            for (var j in typeData) {//遍历sku分类
                var newCom = onSku.slice(0); //复制一个onsku

                for (var k = 0, newTLen = typeData[j].length; k < newTLen; k++) {
                    for (var n = 0, nlen = onSku.length; n < nlen; n++) {
                        if (typeData[j][k].SkuId == onSku[n]) {
                            newCom.splice(n, 1);
                            break;
                        }
                    }
                }
                for (var k = 0, newTLen = typeData[j].length; k < newTLen; k++) {
                    var newComP = newCom.slice(0);
                    newComP.push(typeData[j][k].SkuId);
                    var isBoole = false;
                    for (var i = 0, len = okSku.length; i < len; i++) {
                        var skuids = okSku[i].SkuIds;
                        if (query.inArray(newComP, skuids)) {
                            isBoole = true;
                            break;
                        }
                    }
                    if (!isBoole) errorZ.push(typeData[j][k].SkuId);
                }
            }
            return errorZ;
        },
        query: {
            inArray: function (newarr, oldarr) {//判断一个数组是不是包含另外一个数组！
                if (newarr == '' || !newarr || !oldarr || oldarr == '') return false;
                var oldarrs = newarr.length > oldarr.length ? newarr : oldarr,
                     newarrs = newarr.length > oldarr.length ? oldarr : newarr;
                for (var i = 0; i < newarrs.length; i++) {
                    if ($.inArray(newarrs[i], oldarrs) < 0) return false;
                }
                return true;
            },
            isSameType: function (arrid, id) {//判断前面数组里面有无和后面id同组
                var data = Product.skuGroup.skuData;
                for (var i in data) {
                    var arrboo = false,
                        arridboo = false;
                    for (var j = 0; j < data[i].length; j++) {
                        if ($.inArray(data[i][j].SkuId, arrid) >= 0) arrboo = true;
                        if (data[i][j].SkuId == id) arridboo = true;
                    }
                    if (arrboo && arridboo) return true;
                }
                return false;
            },
            skuConId: function (skus) {//根据选中id，找到组合的id 和价格
                if (!skus || skus.length == 0) return '';
                var Sku = Product.snatchData.SkuCombinations;

                if (Sku.length == 0 || !Sku) return false;
                for (var i = 0; i < Sku.length; i++) {
                    var Skui = Sku[i].SkuIds;
                    if (this.inArray(Skui, skus)) {
                        return Sku[i]
                    };
                };
                return '';
            },
            delRepeat: function (arr) {//去除重复
                var Repeat = []
                for (var i = 0; i < arr.length; i++) {
                    if ($.inArray(arr[i], Repeat) < 0) Repeat.push(arr[i]);
                }
                return Repeat;
            }
        },
        price: function () {
            var skuId = [],
            skuErorr = false,
            dom = $('.left');

            $('.img_box', dom).each(function (i, t) {
                $('a.active', t).length > 0 ?
                 skuId.push($('a.active', t).attr('data-skuid')) :
                 skuErorr = true;
            });
            if (skuErorr) return false;
            var objPrice = this.query.skuConId(skuId);
            if (objPrice == '') return false;
            //var disPrice = this.discount(objPrice);
            var Price = objPrice.Price;
            if (objPrice.Promo_Price > 0) {

                Price = objPrice.Promo_Price;
            }
            //var Price = objPrice.Price,
            //  lowest = objPrice.Promo_Price;

            //需要修改的  第一个 如果选择的了sku那 crawlProduct对象中price则赋值为 sku的price
            //第二个 如果选择的了sku那有限时折扣价格 crawlProduct对象中DiscountPrice则赋值为 sku的Promo_Price
            //将商品的价格 变为sku选择的价格
            // Product.snatchData.Price = Price;

            //将商品的显示折扣价格 变为sku的显示折扣价格
            //Product.snatchData.DiscountPrice = lowest === null ? -1 : lowest;

            // lowest = lowest == 0 || Product.snatchData.DiscountExpiredDate <= 0 ? Price : lowest;
            // disPrice = disPrice == 0 ? Price : disPrice;

            //Price = Math.min(Price, lowest);
            //disPrice = Math.min(Price, disPrice);
            if (Price <= 0 || !Price) return false;

            $("#buyprice").val(Price);
            getpricehui(Price);
            //            $('.DetailsC_Mon', dom).text(Price.toFixed(2));

            // Product.snatchData.payPrice = disPrice;

        },
        discount: function (obj) {
            var vipDiscs = vipDisc;
            var Price = obj.Price;
            if (uGroup > 0) {
                vipDiscs = vipDiscs.v4 > 0 || $('#txtUserName').val() == "flanbian" ? vipDiscs.v4 : vipDiscs.v3 > 0 ? vipDiscs.v3 : vipDiscs.v2 > 0 ? vipDiscs.v2 : vipDiscs.v1 > 0 ? vipDiscs.v1 : 0;
                obj.Vip1Price = obj.Vip1Price > 0 ? obj.Vip1Price * Price : obj.Vip1Price;
                obj.Vip2Price = obj.Vip2Price > 0 ? obj.Vip2Price * Price : obj.Vip2Price;
                obj.Vip3Price = obj.Vip3Price > 0 ? obj.Vip3Price * Price : obj.Vip3Price;
                obj.Vip4Price = obj.Vip4Price > 0 ? obj.Vip4Price * Price : obj.Vip4Price;
            };
            var Promo = obj.Promo_Price <= 0 || Product.snatchData.DiscountExpiredDate <= 0 ? Price : obj.Promo_Price;
            var disPrice = 0;
            if (vipDiscs > 0) {
                disPrice = Price * vipDiscs;
            };
            if (Promo > disPrice && disPrice != 0) {
                $('#VIPPrice').show();
                $('#VIPPrice em').text('￥' + disPrice.toFixed(2));

            } else {
                $('#VIPPrice').hide();
            };
            return disPrice;
        },
        dataImg: function (_th) {
            var dataSrc = $(_th).attr('data-img');
            if (dataSrc != '') {
                var imgSrc = shearImg(250, dataSrc);
                $('#JqzoomImg').attr('src', imgSrc);
                $('.DetailsC_ConImgMin li.on').removeClass('on').find('.zoomThumbActive').removeClass('zoomThumbActive');
                $('.zoomWrapperImage img').attr('src', dataSrc);
            }
            return false;
        },
        addmethod: function () {
            var skuId = '.left',
                _this = this,
                errSku = this.errSku;
            $('.img_box a', skuId).click(function () {
                _this.liclick(this);
                return false;
            });
        },
        liclick: function (_this, isFirst) {
            if ($(_this).hasClass('no_active')) return false;
            if ($(_this).hasClass('active ico_dg')) {
                $(_this).removeClass('active ico_dg');
            } else {
                //$(_this).parents('div.img_box').prev().hide();
                $(_this).addClass('active ico_dg').siblings().removeClass('active ico_dg');

                for (var t = 0; t < prodcutMsg.Skus.length; t++) {
                    var PicUrl = prodcutMsg.Skus[t].PicUrl;
                    if (PicUrl && prodcutMsg.Skus[t].SkuId == $(_this).attr("data-skuid")) {
                        $(".img_big span img").attr("src", PicUrl);
                        //$(".img_big span img").attr("source", PicUrl);
                        //                $("#PicUrl").attr("src",PicUrl);
                    }
                }
                //                isFirst ? '' : this.dataImg(_this);
            };
            this.skuAddHui();
            this.price();
            return false;
        }
    },
    method: function () {
        var skuId = '.left',
            _this = this;

        $('.DetailsC_Textarea', skuId).focus(function () {//备注方法
            if ($.trim($(this).val()).length == 0 || $(this).hasClass('DetailsC_TextareaHui'))
                $(this).removeClass('DetailsC_TextareaHui');
        }).blur(function () {
            if ($.trim($(this).val()).length == 0) $(this).addClass('DetailsC_TextareaHui');
        });

        var NotPrice = $('#notProductPrice');
        if (NotPrice.length > 0) {
            Product.numbers.digital({ dom: NotPrice[0], price: true });
            NotPrice.focus(function () {//商品价格
                if ($(this).hasClass('amc_red')) {
                    $(this).removeClass('amc_red').val('');
                }
            }).blur(function () {
                if ($.trim(this.value).length == 0) {
                    $(this).addClass('amc_red').val('请填写商品价格');
                }
            });
            if (NotPrice.val() != '请填写商品价格' && NotPrice.hasClass('amc_red')) {
                $(this).removeClass('amc_red');
            }
        }

        var NotPrice = $('#DetailsC_Freight');
        if (NotPrice.length > 0) {
            Product.numbers.digital({ dom: NotPrice[0], price: true });
            NotPrice.focus(function () {//运费价格
                if ($(this).hasClass('amc_red')) {
                    $(this).removeClass('amc_red').val('');
                }
            }).blur(function () {
                if ($.trim(this.value).length == 0) {
                    $(this).addClass('amc_red').val('请填写运费');
                }
            });
            if (NotPrice.val() != '请填写运费' && NotPrice.hasClass('amc_red')) {
                $(this).removeClass('amc_red');
            }
        }

        var NotName = $('#notProductName');
        if (NotName.length > 0) {
            NotName.focus(function () {//商品名称
                if ($(this).hasClass('amc_red')) {
                    $(this).removeClass('amc_red').val('');
                }
            }).blur(function () {
                if ($.trim(this.value).length == 0) {
                    $(this).addClass('amc_red').val('请填写商品名称');
                }
            });
            if (NotName.val() != '请填写商品名称' && NotPrice.hasClass('amc_red')) {
                $(this).removeClass('amc_red');
            }
        }


        $('#DetailsCSubmit').click(function () {//增加商品按钮事件

            _this.addSubmit(this);

            return false;
        });

        $('.DetailsC_ConImgMin li').mouseover(function () {
            $(this).addClass('on').siblings('.on').removeClass('on');
        });

        this.numbers.isNumbers($('#quickbuy_float .Buy_Num input'), true);
    },
    addSubmitMess: function (num) {
        var okSku = this.skuGroup.okSku;
        Product.snatchData.Remark = $.trim($('.DetailsC_Textarea').val());
        Product.snatchData.BuyNum = num;
        //crawlProduct.Price = $('#SkuPerv .DetailsC_Mons s').text().match(/\d{1,}(\.\d+)?$/)[0];
    },
    addSubmit: function () {

        var ProductName = $('#notProductName')
        if (ProductName.length > 0) {
            var ProductNameText = $.trim(ProductName.val());
            if (ProductNameText.length == 0 || ProductName.hasClass('amc_red')) {
                return false;
            };
            Product.snatchData.ProductName = ProductNameText;
        }

        var ProductPrice = $('#notProductPrice');
        if (ProductPrice.length > 0) {
            var ProductPriceNum = parseFloat($('#notProductPrice').val());
            if (ProductPrice.hasClass('amc_red')) {
                alert('请填写商品价格');
                return false;
            };
            if (isNaN(ProductPriceNum) || ProductPriceNum == 0) {
                alert('商品价格格式错误,请重新提交。');
                return false;
            };
            Product.snatchData.Price = ProductPriceNum;
        };

        var ProductFreight = $("#DetailsC_Freight");
        if (ProductFreight.length > 0 && !ProductFreight.attr('disabled')) {
            var ProductFreightNum = parseFloat(ProductFreight.val());
            if (ProductFreight.hasClass('amc_red')) {
                alert('请填写运费价格');
                return false;
            };
            if (isNaN(ProductFreightNum)) {
                alert('运费价格格式错误,请重新提交。');
                return false;
            };
            Product.snatchData.Freight = ProductFreightNum;
        }

        var _this = this,
            skuId = '#quickbuy_float',
            skuStr = [],
            skuErorr = false,
            skuHtml = '';
        $('.DetailsC_Sku', skuId).each(function (i, t) {
            if ($('li.on', t).length > 0) {
                skuHtml += (skuHtml == '' ? '' : ' ') + $('li.on a', t).text();
                skuStr.push($('li.on', t).attr('data-skuid'));
            } else {
                $('.DetailsCTi', t).show();
                skuErorr = true;
            }
        });
        if (skuErorr) return false;

        var num = $('#quickbuy_float .Buy_Num input').val();
        if (!/^(0+)?[1-9](\d+)?$/.test(num)) {//验证提交商品数量是否符合
            alert('商品数量提交异常,请重新提交。');
            $('#quickbuy_float .Buy_Num input').val(1);
            return false;
        };
        this.addSubmitMess(num);
        Product.snatchData.DiscountExpiredDate = Product.snatchData.ClientDate;
        var comSku = this.skuGroup.query.skuConId(skuStr);
        comSku = comSku == '' ? '' : comSku.CombinationId;
        Product.snatchData.Description = "";
        //crawlProduct.Description = encodeURIComponent(crawlProduct.Description);
        if (comSku == '' && skuHtml != '') {
            alert('当前商品无库存，请重新选择。'); return false;
        }
        this.submitAjax(comSku, skuHtml);


    },
    submitAjax: function (comSku, skuHtml) {
        var price = Product.snatchData.payPrice,
        snatch = Product.snatchData;
        $.ajax({
            type: "POST",
            url: "/App_Services/wsAddItem.asmx/AddToShoppingCart",
            dataType: "json",
            contentType: "application/json;utf-8",
            data: JSON.stringify({ "json": JSON.stringify(Product.snatchData), "skuStr": skuHtml, "skuComId": comSku }),
            timeout: 20000,
            beforeSend: function () {
                if ($('.BuyYesTop .shopType').length == 0) { $('.shopBuyGoodsYes').show(); $('.shopBuyGoodsNo').hide(); }
                $('#BuyYesUlLoad .BuyYesUlLoad').animate({ marginTop: '0px' }, 100);
                $('#DetailsCSubmit').attr('disabled', 'disabled');
            },
            complete: function () {

            },
            error: function () {
                alert('网络错误，请稍后再试');
                if ($('.BuyYesTop .shopType').length <= 0) { $('.shopBuyGoodsYes').hide(); $('.shopBuyGoodsNo').show(); }
                $('#BuyYesUlLoad .BuyYesUlLoad').animate({ marginTop: '-77px' }, 100);
                $('#DetailsCSubmit').removeAttr('disabled');
            },
            success: function (data) {
                data = data.d || data;
                snatch.SkuComId = comSku;
                snatch.SkuStr = skuHtml;
                snatch.Price = price == 0 || !price ? snatch.Price > snatch.DiscountPrice && snatch.DiscountPrice > 0 ? snatch.DiscountPrice : snatch.Price : price;
                data.Error == '' ? Product.goodsList.addLiHtml(Product.snatchData)
                                : function () {
                                    if ($('.BuyYesTop .shopType').length <= 0) { $('.shopBuyGoodsYes').hide(); $('.shopBuyGoodsNo').show(); };
                                    $('#BuyYesUlLoad .BuyYesUlLoad').animate({ marginTop: '-77px' }, 100);
                                    $('#DetailsCSubmit').removeAttr('disabled');
                                    alert("添加购物车失败！");
                                } ();
            }
        });
    }


};

var property_total = 0;
function add_remark() {
    var property = "";
    var flag = true;
    $('.all_error').show();
    $('.all_error').html('');
    var tmp_price = $("#buyprice").val();
    //        if(buyType!='diy'){
    if (tmp_price <= 0) {
        $("#buyprice").focus();
        $('.all_error').html('<em>请输入商品价格</em>');
        $('#buyprice_text').hide();
        return false;
    } else {
        $('.all_error').html('');
        $('.all_error').hide();
        $('#buyprice_text').text('如系统获取的价格有误，可以手动修改');
        $('#buyprice_text').show();
    }
    var tmp_freight = $("#buyfreight").val();
    if (tmp_freight == '') {
        $("#buyfreight").focus();
        $('.all_error').html('<em>请输入国内运费</em>');
        return false;
    }
    //}        alert(prodcutMsg.Price);
    var sku_arr = "";
    var sku_typenames = [];
    var sku = 1;
    if (prodcutMsg.Skus && prodcutMsg.Skus != "null" && prodcutMsg.Skus.length > 0) {
        for (var n = 0; n < prodcutMsg.Skus.length; n++) {
            if (sku_typenames.indexOf(prodcutMsg.Skus[n].TypeName) < 0) {
                sku_typenames.push(prodcutMsg.Skus[n].TypeName);
            }
        }
        for (var m = 0; m < sku_typenames.length; m++) {
            var temptypeid = "";
            for (var k = 0; k < prodcutMsg.Skus.length; k++) {
                if (prodcutMsg.Skus[k].TypeName == sku_typenames[m]) {
                    temptypeid += prodcutMsg.Skus[k].SkuId + ",";
                }
            }
            temptypeid = temptypeid.substring(0, temptypeid.length - 1);
            sku_arr += sku_typenames[m] + "@" + temptypeid + "|";
        }
        sku_arr = sku_arr.substring(0, sku_arr.length - 1);
        var cut_select_arr = new Array();
        $(".active").each(function (i) {
            cut_select_arr[i] = $(this).attr('data-skuid');
            property += $(this).attr('typename') + ":" + $(this).attr('propertyname') + "\n";
        });
        var temsku_arr = sku_arr.split('|');

        for (var i = 0; i < temsku_arr.length; i++) {
            var tempsky_arr_ch = temsku_arr[i].split('@');
            var tempsky_arr_ch_sku = tempsky_arr_ch[1].split(',');
            var flag = 0;
            for (var j = 0; j < tempsky_arr_ch_sku.length; j++) {
                if (tempsky_arr_ch[i] != "") {
                    if (cut_select_arr.indexOf(tempsky_arr_ch_sku[j]) > -1) {
                        flag = 1;
                    }
                }
            }
            if (flag == 0) {
                $('.all_error').show();
                $('.all_error').html('<em>请选择' + tempsky_arr_ch[0] + '</em>');
                return false;
            }
        }
    }
    var tmp_number = $("#quantity").val();
    if (tmp_number <= 0) {
        $("#quantity").focus();
        $('.all_error').html('<em>请输入数量</em>');
        return false;
    }
    tmp_price = parseFloat(tmp_price);
    tmp_freight = parseFloat(tmp_freight);
    var remark = 'ssss';
    var prop_img = $("#PicUrl").attr("src");
    //    if ($("#prifex").val() == 'AL') {
    //        remark = property;
    //    }
    //                    $('#property_minicart_list').append('<ul>\n\
    //<li class="mimicart_title" name="mimicart_title" style="width:235px;overflow:hidden" remark="' + remark + '" title="' + property + '">' + property + '</li>\n\
    //<li class="mimicart_title mimicart_title_edit" name="mimicart_title_edit" style="display:none" >\n\
    //<span>' + property + '</span>\n\
    //<textarea class="mimicart_title_edit" name="ta_title_edit" style="border:1px solid #ccc;padding:2px;width:225px;font-size:12px;height:15px;" title="可以告诉我们您对商品的特殊要求，如：颜色、尺码等"></textarea>&nbsp;\n\
    //<a href="#nogo" name="confirmed" onclick="confirmed_edit(this)">确定</a>&nbsp;\n\
    //<a href="#nogo" name="cancel" onclick="cancel_edit(this)">取消</a></li>\n\
    //<li class="mimicart_pic" name="mimicart_pic" style="display:none;"><span name="pic">' + prop_img + '</span></li>\n\
    //<li class="mimicart_price" name="mimicart_price"><span name="price">' + tmp_price.toFixed(2) + '</span></li>\n\
    //<li class="mimicart_freight" name="mimicart_freight" style="display:none"><span name="freight">' + tmp_freight.toFixed(2) + '</span></li>\n\
    //<li class="mimicart_number" name="mimicart_number"><span name="number">' + tmp_number + '</span></li>\n\
    //<li class="mimicart_skus" name="mimicart_skus" style="display:none"><span name="skus">' + sku + '</span></li>\n\
    //<li class="mimicart_edit" name="mimicart_edit"><a href="#nogo" onclick="property_desc_delete(this)">删除</a></li></ul>');

    //                    $("#buy_number").val(1);


    var goodname = $("#good_name").val();
    var goodsalerName = $("#nick_name").val();
    var goodsalerUrl = $("#shop_url").val();
    var goodUrl = $("#info_url").val();
    var goodfrom = $("#prifex").val();
    var goodpic = $("#pic_url").val();
    var goodexpprice = tmp_freight;
    var goodsprice = tmp_price;
    var goodsskustr = property;
    var goodsnum = tmp_number;



    $.ajax({
        type: "POST",
        url: "/templets/daigou/Tools/DaiGouCar.ashx",
        data: "Action=addCarone&goodname=" + escape(goodname) + "&goodsalerName=" + goodsalerName + "&goodsalerUrl=" + escape(goodsalerUrl) + "&goodUrl=" + escape(goodUrl) + "&goodfrom=" + goodfrom + "&goodpic=" + goodpic + "&goodexpprice=" + goodexpprice + "&goodsprice=" + goodsprice + "&goodsskustr=" + escape(goodsskustr) + "&goodsnum=" + goodsnum,
        success: function (msg) {
            alert("添加成功！");
            //SuccessManager(goodname, goodsprice, goodexpprice, goodsnum);
            head.GetCartNum();
        }
    });








    /*
    $("tr[id^='property_list'] li").removeClass('select');
    for(x in property_str){
    property_str[x]='';
    }
    */
    property_desc_length();
}


function SuccessManager(name, priceUsd, freightusd, amount) {

    $("#successcontent").find("[data-name=title]").text(name);
    $("#successcontent").find("[data-name=price]").text(priceUsd);
    $("#successcontent").find("[data-name=shipping]").text(freightusd);
    $("#successcontent").find("[data-name=qty]").text(amount);
    $("#successcontent").show();
    $("#content").hide();
}
function property_desc_length() {
    property_desc = '';
    property_total = 0;
    $('#property_minicart_list ul').each(function () {
        property_total += parseInt($(this).find('span[name="number"]').text());
        property_desc += $(this).find('li[name=mimicart_title]').text() + "\n";
    });
    $('#property_minicart_total .or_font').html(property_total);
    return property_desc.length;
}

function property_desc_delete(obj) {
    $(obj).parent().parent().remove();
    desc_max_length = 200 - property_desc_length();
    $('#desc').keyup();
}
function batch_send_cart() {
    var postUrl = '';
    $("#error_msg").text('');
    if (property_total <= 0) {
        $('#buyremark_err_msg').text('请选择你要购买的商品');
        return false;
    }
    var batch_data = {
        title: $('#buytitle').val(),
        nick_name: $('#nick_name').val(),
        info_url: $('#info_url').val(),
        shop_url: $('#shop_url').val(),
        pic_url: $('#pic_url').val(),
        prifex: $("#prifex").val(),
        //            goods_id:$("#goods_id").val(),
        //            property:$("#property").val(),
        t_freight: $("#buyfreight").val(),
        item: {}
    };
    $('#property_minicart_list ul').each(function (i) {
        price = parseFloat($(this).find('span[name="price"]').text());
        freight = parseFloat($(this).find('span[name="freight"]').text());
        number = parseFloat($(this).find('span[name="number"]').text());
        //desc = $(this).find('li[name=mimicart_title]').attr('remark');
        desc = $(this).find('li[name=mimicart_title]').text();
        pic = $(this).find('li[name=mimicart_pic]').text();
        skus = $(this).find('li[name=mimicart_skus]').text();
        if (price == 0) {
            alert('商品单价不能为0');
            return false;
        }

        if (number == 0) {
            alert('购买数量不能为0');
            return false;
        }
        // 淘宝商品代购不传desc - 即商品属性
        if ($('#prifex').val() == 'TB' && buyType != 'diy') {
            desc = '';
        }
        batch_data['item'][i] = {
            pic: pic,
            price: price,
            freight: freight,
            number: number,
            skus: skus,
            desc: desc + $('#desc').val().replace(/如您购买的商品含有多种款式、尺寸、颜色，请您根据商品页面上的分类描述，在此备注说明相关款式。/, '')
        };
    });
    $.ajax({
        url: postUrl,
        type: 'post',
        data: batch_data,
        dataType: 'json',
        //timeout : 1000,
        error: function () {
            alert('网络繁忙，请稍候重试。');
        },
        success: function (result) {
            if (result.msg == 'err') {
                var info = result.info ? result.info : '添加失败,请重试';
                alert(info);
                return false;
            }
            //$("#dialog table").hide();
            //$("#quickbuy_div_one").hide();
            //$("#quickbuy_float").hide();
            //$("#p_imitation").hide();
            //alert(result.info.count);
            $("#quickbuy_ok").show();
            $("#quickbuy_ok .or_font").eq(0).text(result.info.count);
            //$("#quickbuy_ok .or_font").eq(1).text(result.info.money);
            $('#send_card_ok').dialog({
                title: "添加成功",
                width: 480,
                modal: true,
                draggable: false,
                resizable: false
            });
            //$("#recommend").show();
        }
    });
}
function test() {
    if ($("#property_minicart_list ul").length == 0) {
        alert('商品清单没有发现商品！');
        return;
    }

    var goodname = $("#good_name").val();
    var goodsalerName = $("#nick_name").val();
    var goodsalerUrl = $("#shop_url").val();
    var goodUrl = $("#info_url").val();
    var goodfrom = $("#prifex").val();
    var goodpic = $("#pic_url").val();
    var goodexpprice = $("#buyfreight").val();

    var datalist = "";
    $("#property_minicart_list ul").each(function (i) {
        datalist += $(this).children().eq(0).text() + "|";
        datalist += $(this).children().eq(3).children().text() + "|";
        datalist += $(this).children().eq(5).children().text() + ",";
    });
    $.ajax({
        type: "POST",
        url: "/templets/daigou/Tools/DaiGouCar.ashx",
        data: "Action=addCar&goodname=" + goodname + "&goodsalerName=" + goodsalerName + "&goodsalerUrl=" + escape(goodsalerUrl) + "&goodUrl=" + escape(goodUrl) + "&goodfrom=" + goodfrom + "&goodpic=" + goodpic + "&goodexpprice=" + goodexpprice + "&datalist=" + datalist,
        success: function (msg) {
            $("#carnum").text(msg);
            art.dialog({ id: 'send_card_ok', title: '添加成功', content: document.getElementById('send_card_ok'), lock: true, fixed: true });
        }
    });




    // $('#send_card_ok').dialog({
    //                    title:"添加成功",
    //                    width:500,
    //                    modal:true,
    //                    draggable:false,
    //                    resizable: false
    //   });
}

function getpricehui(price) {
    var mh = $("#huilv").val();
    $("#mprice").text(changeTwoDecimal(price / mh));
}
function changeTwoDecimal(x) {
    var f_x = parseFloat(x);
    if (isNaN(f_x)) {
        return false;
    }
    f_x = Math.round(f_x * 100) / 100;
    return f_x;
}


function bookgoods() {
    var goodname = $("#good_name").val();
    var goodsalerName = $("#nick_name").val();
    var goodsalerUrl = $("#shop_url").val();
    var goodUrl = $("#info_url").val();
    var goodpic = $("#pic_url").val();
    $.ajax({
        type: "POST",
        url: "/templets/daigou/Tools/DaiGouCar.ashx",
        data: "Action=bookgood&goodname=" + goodname + "&goodsalerName=" + goodsalerName + "&goodsalerUrl=" + escape(goodsalerUrl) + "&goodUrl=" + escape(goodUrl) + "&goodpic=" + goodpic + "&goodsprice=" + 0,
        success: function (msg) {
            if (msg == "1") {
                art.dialog({ id: 'book_ok', title: '收藏成功', content: '收藏成功', lock: true, fixed: true });
            } else if (msg == "3") {
                art.dialog({ id: 'book_ok', title: '已经存在', content: '已经存在', lock: true, fixed: true });

            } else {
                art.dialog({ id: 'book_ok', title: '收藏失败', content: '收藏失败', lock: true, fixed: true });
            }
        }
    });

}