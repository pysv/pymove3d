#encoding=utf8
from starflyer import Handler, redirect, asjson
from camper import BaseForm, db, BaseHandler, ensure_barcamp, logged_in, is_admin, is_participant
from base import BarcampView
from wtforms import *
from sfext.babel import T

class BlogAddForm(BaseForm):
    """form for adding a new blog link"""
    title = TextField(T("Post Title"), [validators.Length(max=1000), validators.Required()],
                description = T('title of the blog post you are linking to')
    )
    url = TextField(T("Post URL"), [validators.Length(max=1000), validators.Required()],
                description = T('URL of the blog post you want to link to')
    )
    

class PlanningPadView(BaseHandler):
    """shows the main page of a barcamp"""

    template = "barcamp/pad.html"

    @ensure_barcamp()
    def get(self, slug = None):
        """render the view"""
        if not self.barcamp.planning_pad_public and not self.is_admin:
            self.flash(self._(self._('You are not allowed to access this page as you are not an administrator of this barcamp.')), category="danger")
            return redirect(self.url_for("barcamp", slug = self.barcamp.slug))
        return self.render(
            view = BarcampView(self.barcamp, self), 
            barcamp = self.barcamp,
            show_public_switch = True,
            pad = self.barcamp.planning_pad,
            title = self.barcamp.name,
            **self.barcamp)

class DocumentationPadView(BaseHandler):
    """shows documentation pad"""

    template = "barcamp/docs.html"

    @ensure_barcamp()
    def get(self, slug = None):
        """render the view"""
        form = BlogAddForm(config = self.config)
        posts = self.barcamp.blogposts
        uids = set([p['user_id'] for p in posts])
        users = self.app.module_map['userbase'].get_users_by_ids(list(uids))
        usermap = dict([(str(u._id), u) for u in users])

        return self.render(
            view = BarcampView(self.barcamp, self), 
            barcamp = self.barcamp,
            posts = posts,
            usermap = usermap,
            pad = self.barcamp.documentation_pad,
            title = self.barcamp.name,
            form = form,
            **self.barcamp)

    @ensure_barcamp()
    @is_participant()
    def post(self, slug = None):
        form = BlogAddForm(self.request.form, config = self.config)
        if form.validate():
            blog = {
                'title' : form.data['title'],
                'url' : form.data['url'],
                'user_id' : self.user._id,
            }
            self.barcamp.blogposts.append(blog)
            self.barcamp.save()
            self.flash(self._("Your blog post has been posted."), category="success")
            return redirect(self.url_for("barcamp_documentation_pad", slug = slug))


        return self.get(slug)

    @ensure_barcamp()
    @asjson()
    def delete(self, slug = None):
        idx = int(self.request.form['idx']) # index in list
        del self.barcamp.blogposts[idx]
        self.barcamp.put()
        return {'status' : 'success'}



class PadPublicToggleView(BaseHandler): 
    """handler for toggeling the public switch for the planning pad"""

    @ensure_barcamp()
    @logged_in()
    @is_admin()
    def post(self, slug = None):
        self.barcamp.planning_pad_public = not self.barcamp.planning_pad_public
        self.barcamp.put()
        return redirect(self.url_for("barcamp_planning_pad", slug = self.barcamp.slug))


