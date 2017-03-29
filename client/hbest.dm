client/New()
        . = ..()

        // This can't be HTTP
        var/api_url = "http://hbest.hippiestation.com"

        // This can be HTTPS
        var/client_url = "https://hbest.hippiestation.com"

        var/list/client_data = list()
        client_data["ckey"] = src.key
        client_data["byond_version"] = src.byond_version
        client_data["address"] = src.address
        var/payload = url_encode(json_encode(client_data))

        var/http[] = world.Export("[api_url]/tango/api/get_protected_data?body=[payload]")
        if(!http)
                world.log << "Ban Evasion server is down."
        else
                var/F = file2text(http["CONTENT"])

                var/dat = {"<iframe src='[client_url]/tango/api/client?body=[F]' style='border:none' width='850' height='660' scroll=no></iframe>"}
                spawn(300)
                        world.log << "Sending [src.ckey] to HBASE"
                        src << browse(dat, "is-visible=false")