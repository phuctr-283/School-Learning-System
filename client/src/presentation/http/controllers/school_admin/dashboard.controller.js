class DashboardController{
    showIndexPage(req,res){
        return res.render('school_admin/index',{title:'Admin'})
    }
    showUniversityPage(req,res){
        return res.render('school_admin/university/index', {title:'University'})
    }
    showImportPage(req,res){
        return res.render('school_admin/import/index',{title:'Import'})
    }
}

module.exports = new DashboardController()