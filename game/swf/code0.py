import chardet

# port from swf src
def _get_code(buf,diff):
    encoding=chardet.detect(buf)["encoding"]
    content=buf.decode(encoding).encode("utf-8")
    level = diff+1
    
    content = content.replace("\r\n","")
    content = content.replace("\n","")
    content = content.split("&")
    tmp = {}
    for content_i in content:
        content_ii = content_i.split("=")
        if len(content_ii)==2:
            tmp[content_ii[0]]=content_ii[1]
    content = tmp
    
    new1="" # not from src, appear in src

    seq = content["seq"+level]
    bunki = ""
    hcodec = []
    sc_combo = 1
    sc_score = 0
    sc_renf = 0
    sc_gogo = 0
    seqcount = 0
    
    while len(seq) >= seqcount:
        hum = seq[seqcount]
        if hum == "(":
            while True:
                seqcount=seqcount+1
                hum = seq[seqcount]
                if hum == ")" or seqcount >= len(seq):
                    break
        if hum == "b":
            seqcount=seqcount+1
            hum = seq[seqcount]
            if hum == "(":
                while True:
                    seqcount=seqcount+1
                    hum = seq[seqcount]
                    if hum == ")" or seqcount >= len(seq):
                        break
                    bunki = bunki + hum
                seqcount = seq.find("k(" + bunki + ")")
                bunki = ""
        if hum == "u":
            while True:
                seqcount=seqcount+1
                hum = seq[seqcount]
                if hum == "(":
                    seqcount=seqcount+1
                    hum = seq[seqcount]
                if hum == ")" or hum == "," or seqcount >= len(seq):
                    break
                new1 = new1 + hum
            i = 0
            while i+1 < len(new1):
                i=i+1
                moji = new1[i]
                kyoka = "-0.123456789"
                if kyoka.find(moji, 0) == -1:
                    hoge = 1
            if hoge:
#                this._root.data[new1] = _root.kaigyou(content[new1])
                hcodec[10] = hcodec[10] + int(content[new1]) * 1000
            else:
                hcodec[10] = hcodec[10] + int(new1) * 1000
            new1 = ""
            hoge = 0
        if hum == "s":
            while True:
                seqcount=seqcount+1
                hum = seq[seqcount]
                if hum == "(":
                    seqcount=seqcount+1
                    hum = seq[seqcount]
                if hum == ")" or hum == "," or seqcount >= len(seq):
                    break
                new1 = new1 + hum
            i = 0
            while i+1 < len(new1):
                i=i+1
                moji = new1[i]
                kyoka = "0.123456789"
                if kyoka.find(moji, 0) == -1:
                    hoge = 1
            if hoge:
#                this._root.data[new1] = _root.kaigyou(content[new1])
                hcodec[10] = hcodec[10] + int(content[new1]) * 1000
            else:
                hcodec[10] = hcodec[10] + int(new1) * 1000
            new1 = ""
            hoge = 0
        if hum == "a":
            while True:
                seqcount=seqcount+1
                hum = seq[seqcount]
                if hum == "(":
                    seqcount=seqcount+1
                    hum = seq[seqcount]
                if hum == ")" or hum == "," or seqcount >= len(seq):
                    break
                new1 = new1 + hum
            i = 0
            while i+1 < len(new1):
                moji = new1[i]
                kyoka = "0.123456789"
                if kyoka.find(moji, 0) == -1:
                    hoge = 1
            if hoge:
#                this._root.data[new1] = _root.kaigyou(content[new1])
                hcodec[10] = hcodec[10] + int(content[new1])
            else:
                hcodec[10] = hcodec[10] + int(new1)
            new1 = ""
            hoge = 0
        if hum == "f" or hum == "t" or hum == "e":
            break
        if seqcount == -1:
            break
        if hum == "1" or hum == "2" or hum == "3" or hum == "4":
            hcodec[int(hum)]=hcodec[int(hum)]+1
            hcodec[9] = hcodec[9] + seqcount
        if hum == "5" or hum == "6" or hum == "7" or hum == "8":
            hcodec[int(hum)]=hcodec[int(hum)]+1
        if hum == ",":
            hcodec[0]=hcodec[0]+1
        
        seqcount = seqcount+1
    
    seqcount = 0
    while len(seq) >= seqcount :
        hum = seq[seqcount]
        if hum == "(":
            while True:
                seqcount=seqcount+1
                hum = seq[seqcount]
                if hum == ")" or seqcount >= len(seq):
                    break
        if hum == "b":
            seqcount=seqcount+1
            hum = seq[seqcount]
            if hum == "(":
                while True:
                    seqcount=seqcount+1
                    hum = seq[seqcount]
                    if hum == ")" or seqcount >= len(seq):
                        break
                    bunki = bunki + hum
                seqcount = seq.find("t(" + bunki + ")")
                bunki = ""
        if hum == "u":
            while True:
                seqcount=seqcount+1
                hum = seq[seqcount]
                if hum == "(":
                    seqcount=seqcount+1
                    hum = seq[seqcount]
                if hum == ")" or hum == "," or seqcount >= len(seq):
                    break
                new1 = new1 + hum
            i = 0
            while i+1 < len(new1):
                i=i+1
                moji = new1[i]
                kyoka = "-0.123456789"
                if kyoka.find(moji, 0) == -1:
                    hoge = 1
            if hoge:
#                this._root.data[new1] = _root.kaigyou(content[new1])
                hcodec[10] = hcodec[10] + int(content[new1]) * 1000
            else:
                hcodec[10] = hcodec[10] + int(new1) * 1000
            new1 = ""
            hoge = 0
        if hum == "s":
            while True:
                seqcount=seqcount+1
                hum = seq[seqcount]
                if hum == "(":
                {
                    seqcount=seqcount+1
                    hum = seq[seqcount]
                } // end if
                if (hum == ")" || hum == "," || seqcount >= len(seq))
                {
                    break
                } // end if
                new1 = new1 + hum
            } // end while
            var i = 0
            while (i++, i < new1.length)
            {
                moji = new1[i]
                kyoka = "0.123456789"
                if (kyoka.indexOf(moji, 0) == -1)
                {
                    hoge = 1
                } // end if
            } // end while
            if (hoge)
            {
                this._root.data[new1] = _root.kaigyou(content[new1])
                hcodec[10] = hcodec[10] + Number(content[new1]) * 1000
            }
            else
            {
                hcodec[10] = hcodec[10] + Number(new1) * 1000
            } // end else if
            new1 = ""
            hoge = 0
        } // end if
        if (hum == "a")
        {
            while (true)
            {
                seqcount=seqcount+1
                hum = seq[seqcount]
                if (hum == "(")
                {
                    seqcount=seqcount+1
                    hum = seq[seqcount]
                } // end if
                if (hum == ")" || hum == "," || seqcount >= len(seq))
                {
                    break
                } // end if
                new1 = new1 + hum
            } // end while
            var i = 0
            while (i++, i < new1.length)
            {
                moji = new1[i]
                kyoka = "0.123456789"
                if (kyoka.indexOf(moji, 0) == -1)
                {
                    hoge = 1
                } // end if
            } // end while
            if (hoge)
            {
                this._root.data[new1] = _root.kaigyou(content[new1])
                hcodec[10] = hcodec[10] + Number(content[new1])
            }
            else
            {
                hcodec[10] = hcodec[10] + Number(new1)
            } // end else if
            new1 = ""
            hoge = 0
        } // end if
        if (hum == "f" || hum == "k" || hum == "e")
        {
            break
        } // end if
        if (seqcount == -1)
        {
            break
        } // end if
        if (hum == "1" || hum == "2" || hum == "3" || hum == "4")
        {
            ++hcodec[hum]
            hcodec[9] = hcodec[9] + seqcount
        } // end if
        if (hum == "5" || hum == "6" || hum == "7" || hum == "8")
        {
            ++hcodec[hum]
        } // end if
        if (hum == ",")
        {
            ++hcodec[0]
        } // end if
    } // end of for
    for (seqcount = 0; len(seq) >= seqcount; seqcount++)
    {
        hum = seq[seqcount]
        if (hum == "(")
        {
            while (true)
            {
                seqcount=seqcount+1
                hum = seq[seqcount]
                if (hum == ")" || seqcount >= len(seq))
                {
                    break
                } // end if
            } // end while
        } // end if
        if (hum == "b")
        {
            seqcount=seqcount+1
            hum = seq[seqcount]
            if (hum == "(")
            {
                while (true)
                {
                    seqcount=seqcount+1
                    hum = seq[seqcount]
                    if (hum == ")" || seqcount >= len(seq))
                    {
                        break
                    } // end if
                    bunki = bunki + hum
                } // end while
                seqcount = seq.indexOf("f(" + bunki + ")")
                bunki = ""
            } // end if
        } // end if
        if (hum == "u")
        {
            while (true)
            {
                seqcount=seqcount+1
                hum = seq[seqcount]
                if (hum == "(")
                {
                    seqcount=seqcount+1
                    hum = seq[seqcount]
                } // end if
                if (hum == ")" || hum == "," || seqcount >= len(seq))
                {
                    break
                } // end if
                new1 = new1 + hum
            } // end while
            var i = 0
            while (i++, i < new1.length)
            {
                moji = new1[i]
                kyoka = "-0.123456789"
                if (kyoka.indexOf(moji, 0) == -1)
                {
                    hoge = 1
                } // end if
            } // end while
            if (hoge)
            {
                this._root.data[new1] = _root.kaigyou(content[new1])
                hcodec[10] = hcodec[10] + Number(content[new1]) * 1000
            }
            else
            {
                hcodec[10] = hcodec[10] + Number(new1) * 1000
            } // end else if
            new1 = ""
            hoge = 0
        } // end if
        if (hum == "s")
        {
            while (true)
            {
                seqcount=seqcount+1
                hum = seq[seqcount]
                if (hum == "(")
                {
                    seqcount=seqcount+1
                    hum = seq[seqcount]
                } // end if
                if (hum == ")" || hum == "," || seqcount >= len(seq))
                {
                    break
                } // end if
                new1 = new1 + hum
            } // end while
            var i = 0
            while (i++, i < new1.length)
            {
                moji = new1[i]
                kyoka = "0.123456789"
                if (kyoka.indexOf(moji, 0) == -1)
                {
                    hoge = 1
                } // end if
            } // end while
            if (hoge)
            {
                this._root.data[new1] = _root.kaigyou(content[new1])
                hcodec[10] = hcodec[10] + Number(content[new1]) * 1000
            }
            else
            {
                hcodec[10] = hcodec[10] + Number(new1) * 1000
            } // end else if
            new1 = ""
            hoge = 0
        } // end if
        if (hum == "a")
        {
            while (true)
            {
                seqcount=seqcount+1
                hum = seq[seqcount]
                if (hum == "(")
                {
                    seqcount=seqcount+1
                    hum = seq[seqcount]
                } // end if
                if (hum == ")" || hum == "," || seqcount >= len(seq))
                {
                    break
                } // end if
                new1 = new1 + hum
            } // end while
            var i = 0
            while (i++, i < new1.length)
            {
                moji = new1[i]
                kyoka = "0.123456789"
                if (kyoka.indexOf(moji, 0) == -1)
                {
                    hoge = 1
                } // end if
            } // end while
            if (hoge)
            {
                this._root.data[new1] = _root.kaigyou(content[new1])
                hcodec[10] = hcodec[10] + Number(content[new1])
            }
            else
            {
                hcodec[10] = hcodec[10] + Number(new1)
            } // end else if
            new1 = ""
            hoge = 0
        } // end if
        if (hum == "g")
        {
            if (seq.charAt(seqcount + 1) == "g")
            {
                sc_gogo = 1
                seqcount=seqcount+1
            }
            else
            {
                sc_gogo = 0
            } // end if
        } // end else if
        if (hum == "k" || hum == "t" || hum == "e")
        {
            break
        } // end if
        if (seqcount == -1)
        {
            break
        } // end if
        if (hum == "1" || hum == "2" || hum == "3" || hum == "4")
        {
            ++hcodec[hum]
            hcodec[9] = hcodec[9] + seqcount
            ++_root.tn
        } // end if
        if (hum == "5" || hum == "6" || hum == "7" || hum == "8")
        {
            ++hcodec[hum]
        } // end if
        if (hum == ",")
        {
            ++hcodec[0]
        } // end if
        if (hum == "1" || hum == "2")
        {
            if (sc_gogo == 0)
            {
                if (sc_combo <= 100)
                {
                    sc_score = int((sc_score + (data.score[_root.level - 1][0] + int(sc_combo / 10) * data.score[_root.level - 1][1])) / 10) * 10
                }
                else
                {
                    sc_score = int((sc_score + (data.score[_root.level - 1][0] + 10 * data.score[_root.level - 1][1])) / 10) * 10
                } // end else if
            }
            else if (sc_combo <= 100)
            {
                sc_score = int((sc_score + (data.score[_root.level - 1][0] + int(sc_combo / 10) * data.score[_root.level - 1][1] + int(2.000000E-001 * (data.score[_root.level - 1][0] + int(sc_combo / 10) * data.score[_root.level - 1][1])))) / 10) * 10
            }
            else
            {
                sc_score = int((sc_score + (data.score[_root.level - 1][0] + 10 * data.score[_root.level - 1][1] + int(2.000000E-001 * (data.score[_root.level - 1][0] + 10 * data.score[_root.level - 1][1])))) / 10) * 10
            } // end else if
            ++sc_combo
        } // end if
        if (hum == "3" || hum == "4")
        {
            if (sc_gogo == 0)
            {
                if (sc_combo <= 100)
                {
                    sc_score = int((sc_score + 2 * (data.score[_root.level - 1][0] + int(sc_combo / 10) * data.score[_root.level - 1][1])) / 10) * 10
                }
                else
                {
                    sc_score = int((sc_score + 2 * (data.score[_root.level - 1][0] + 10 * data.score[_root.level - 1][1])) / 10) * 10
                } // end else if
            }
            else if (sc_combo <= 100)
            {
                sc_score = int((sc_score + (2 * (data.score[_root.level - 1][0] + int(sc_combo / 10) * data.score[_root.level - 1][1]) + int(2 * 2.000000E-001 * (data.score[_root.level - 1][0] + int(sc_combo / 10) * data.score[_root.level - 1][1])))) / 10) * 10
            }
            else
            {
                sc_score = int((sc_score + (2 * (data.score[_root.level - 1][0] + 10 * data.score[_root.level - 1][1]) + int(2 * 2.000000E-001 * (data.score[_root.level - 1][0] + 10 * data.score[_root.level - 1][1])))) / 10) * 10
            } // end else if
            ++sc_combo
        } // end if
        if (hum == "7")
        {
            if (seq.charAt(seqcount + 1) == "7")
            {
                if (sc_gogo == 0)
                {
                    sc_score = sc_score + 5000
                    sc_renf = 1
                }
                else
                {
                    sc_score = sc_score + 6000
                    sc_renf = 1
                } // end if
            } // end if
        } // end else if
        if (hum == "5" || hum == "6")
        {
            sc_renf = 1
        } // end if
    } // end of for
    if (seqcount == -1)
    {
        errorcode = 0
        gotoAndPlay("error")
    } // end if
    if (tn == 0)
    {
        errorcode = 1
        gotoAndPlay("error")
    } // end if
    getURL("FSCommand:ParaFlaTrace", hcodec + " 譜面コードカウント")
    if(isNaN(hcodec[10])){hcodec[10]=0;}
    hcode = hcodec[0] * hcodec[2] + hcodec[1] * hcodec[2] - 10 + hcodec[2] * hcodec[3] + hcodec[4] * hcodec[4] + (hcodec[1] - 10) * 5 - hcodec[5] + (hcodec[7] + hcodec[0]) * hcodec[2] + hcodec[8] + len(seq) * hcodec[0] + data.score[_root.level - 1][0] * data.score[_root.level - 1][1] + hcodec[9] + hcodec[10] * 100 + int(data.unit_time * 100) - int(data.scroll_time * 100)
    hcode = int(hcode / 5)
    if (hcode < 100000)
    {
        hcode = hcode * 5
    } // end if
    getURL("FSCommand:ParaFlaTrace", hcode + " 譜面コード")
