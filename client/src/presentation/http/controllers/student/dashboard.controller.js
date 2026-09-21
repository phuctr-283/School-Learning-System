class DashboardController{
    showIndexPage(req,res){
        return res.render('student/index',{title:'Dashboard'})
    }
}

module.exports = new DashboardController()