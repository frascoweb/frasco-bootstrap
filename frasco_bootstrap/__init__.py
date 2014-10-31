from frasco import Feature, hook, current_context
from frasco.templating import FileLoader
from jinja2 import PackageLoader
import os


class BootstrapFeature(Feature):
    name = "bootstrap"
    requires = ["assets"]
    defaults = {"auto_assets": True,
                "with_jquery": True,
                "with_fontawesome": False,
                "fluid_layout": False}

    def init_app(self, app):
        path = os.path.dirname(__file__)
        app.jinja_env.macros.register_package(__name__, prefix="bootstrap")
        app.jinja_env.loader.feature_loaders.append(PackageLoader(__name__))
        app.jinja_env.loader.set_layout_alias("bootstrap_layout.html")

        app.assets.register({
            "bootstrap-cdn": [
                "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css",],
            "bootstrap-theme-cdn": [
                "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"],
            "bootstrap-js-cdn": [
                "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"],
            "bootstrap-all-cdn": [
                "@bootstrap-cdn",
                "@bootstrap-theme-cdn",
                "@bootstrap-js-cdn"],
            "jquery-cdn": [
                "https://code.jquery.com/jquery-2.1.1.min.js"],
            "jquery-bootstrap-all-cdn": [
                "@jquery-cdn",
                "@bootstrap-all-cdn"],
            "font-awesome-cdn": [
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css"]})

        if self.options["auto_assets"]:
            if self.options["with_fontawesome"]:
                app.features.assets.add_default("@font-awesome-cdn")
            if self.options["with_jquery"]:
                app.features.assets.add_default("@jquery-bootstrap-all-cdn")
            else:
                app.features.assets.add_default("@bootstrap-all-cdn")

    @hook()
    def before_request(self):
        current_context["bs_layout_fluid"] = self.options["fluid_layout"]