

class Job():
    def __init__(self, source):
        self.source = source
        plugin_manager = PluginManager()
        self.plugins = plugin_manager.get_plugins()

        return

    def run(self):

        for(plugin in self.plugins):
            plugin.run()

        sys.stdout.write(' \b')
        pipe_out, pipe_in = os.pipe()
        stdout = os.dup(1)
        os.dup2(pipe_in, 1)

        def more_data():
            r, _, _ = select.select([pipe_out], [], [], 0)
            return bool(r)

        def read_pipe():
            while more_data():
                logger.debug(os.read(pipe_out, 1024).decode('utf-8'))


        outbox_path = '/usr/ichnosat/data_local/outbox/'

        for dName, sdName, fList in os.walk(inDIR):
            for fileName in fList:
                if fnmatch.fnmatch(fileName, pattern):  # Match search string
                    try:
                        product_name = self.source.split('/')[-2]



                        destination = outbox_path + product_name + "-" + plugin_name + '/'
                        if not os.path.exists(destination):
                            os.makedirs(destination)
                        cdll.LoadLibrary(plugin_path)
                        libc = CDLL(plugin_path)
                        productPath = self.source.encode('utf-8')
                        destinationPath = destination.encode('utf-8')
                        libc.process.argtypes = [c_char_p]
                        libc.process(productPath, destinationPath)
                        os.dup2(stdout, 1)
                        read_pipe()
                    except ValueError:
                        logger.debug("Failed scientific-processor plugin with name: " + plugin_name)
                        # shutil.rmtree(self.source)