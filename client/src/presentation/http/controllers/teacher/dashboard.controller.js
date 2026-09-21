class DashboardController{
    showIndexPage(req,res){
        return res.render('teacher/index',{title:'Dashboard'})
    }
    showImportPage(req,res){
        return res.render("teacher/import/index",{title:"Import"})
    }
}

module.exports = new DashboardController()