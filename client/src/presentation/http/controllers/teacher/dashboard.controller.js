class DashboardController{
    showIndexPage(req,res){
        return res.render('teacher/index',{title:'Dashboard'})
    }

}

module.exports = new DashboardController()