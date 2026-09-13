const AccountLevel = require("../../../domain/enums/account_level");

function requireAccountLevel(...levels) {
  return (req, res, next) => {
    const user = req.session?.user;
    if (!user) {
      return res.redirect("/");
    }
    if (user.account_level === undefined || user.account_level === null) {
      return res.status(403).render("errors/403", {
        title: "Không có quyền truy cập",
      });
    }
    if (!Object.values(AccountLevel).includes(user.account_level)) {
      return res.status(403).render("errors/403", {
        title: "Không có quyền truy cập",
      });
    }
    if (!levels.includes(user.account_level)) {
      return res.status(403).render("errors/403", {
        title: "Không có quyền truy cập",
      });
    }
    return next();
  };
}

module.exports = requireAccountLevel;
