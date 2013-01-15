$.fn.uploader = (opts = {}) ->
    file_completed = false     
    myfilename = null          

    # show a sponsor
    sponsor = (widget, json) ->
        $(widget).find(".upload-area").hide()
        img = $("<img>").attr(
            "src" :  json.url
            "width" : "100px"
        )
        $(widget).find(".upload-value-id").val(json.asset_id)
        $(widget).find(".preview-area").children().remove()
        $(widget).find(".preview-area").append(img).show()
        
    init = () ->
        url = $(this).data("url")
        postproc = $(this).data("postproc")
        widget = this
        uploader = new qq.FileUploaderBasic(
            button: $(widget).find(".uploadbutton")[0]
            action: url
            multiple: false
            sizeLimit: 10*1024*1024
            allowedExtensions: ['jpg', 'jpeg', 'png', 'gif']
            onProgress: (id, filename, loaded, total) ->
                perc = parseInt(Math.floor(loaded/total*100))+"%"
                $(widget).find(".progressbar .progress").css("width", perc)
            onSubmit: (id, filename) ->
                $(widget).find(".progressbar").show()
                $(widget).find(".preview-area").hide()
            onComplete: (id, filename, json) ->
                if json.error
                    file_completed = false
                    myfilename = null
                    alert(json.msg)
                    $(widget).find(".upload-area").show()
                    $(widget).find(".progressbar").hide()
                    return false
                if json.success
                    file_completed = true
                    if json.redirect
                        window.location = json.redirect
                        return
                    if json.parent_redirect
                        window.parent.window.location = json.parent_redirect
                        window.close()
                        return
                    if postproc
                        if postproc=="sponsor"
                            sponsor(widget, json)
                    $(widget).find(".upload-area").show()
                    $(widget).find(".progressbar").hide()
        )
    $(this).each(init)
    this

$(document).ready( () ->
    $(".upload-widget").uploader()

    # live edit fields
    $('[data-toggle="editfield"]').click( () ->
        $(this).hide();
        p = $(this).closest(".editfield")
        f = $(p).find(".edit").show()
    )
    $('[data-close="editfield"]').live("click", () ->
        $(this).closest(".edit").hide();
        p = $(this).closest(".editfield")
        f = $(p).find(".value").show()
        false
    )
    $('form.edit').live("submit", () ->
        $(this).closest(".edit").hide();
        p = $(this).closest(".editfield")
        f = $(p).find(".value").show()
        alert("Gespeichert")
        false
    )

    $('[data-action="set-layout"]').click( () ->
        layout = $(this).data("layout")
        url = $(this).attr("href")
        that = this
        $.ajax 
            url: url
            type: "POST"
            data: 
                layout: layout
            success: (data) ->
                $(that).closest(".barcamp-page")
                .removeClass("layout-left")
                .removeClass("layout-default")
                .removeClass("layout-right")
                .addClass("layout-"+data.layout)

        return false
    )

    # asset deletion
    $(".asset-delete").click( () ->
        confirm_message = $(this).data("confirm")
        url = $(this).data("url")
        idx =$(this).data("idx") # for sponsor logos
        if confirm(confirm_message)
            $.ajax(
                url: url
                type: "POST"
                data:
                    method: "delete"
                    idx: idx
                success: () ->
                    window.location.reload()
            )
        else
            return
    )

    $("#blog-add-button").click( () -> 
        $("#blog-add-button-container").slideUp();
        $("#blog-add-form").slideDown();
    )
    $("#blog-add-cancel-button").click( () -> 
        $("#blog-add-form")[0].reset();
        $("#blog-add-button-container").slideDown();
        $("#blog-add-form").slideUp();
        return false;
    )
    $(".blog-delete-button").click( () -> 
        msg = $(this).data("msg")
        idx = $(this).data("idx")
        url = $("#blog-add-form").attr("action")
        if confirm(msg)
            $.ajax(
                url: url
                type: "POST"
                data:
                    method: "delete"
                    idx: idx
                success: () ->
                    window.location.reload()
            )
        false
    )

)


